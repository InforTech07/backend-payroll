"""
    serializers for company 
"""
from rest_framework import serializers

from apps.company.models import Company
from apps.user.models import User
from django.contrib.auth.hashers import make_password
from apps.user.serializers import UserModelSerializer


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the company model.
    """
    user = UserModelSerializer(read_only=True)
    #username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    create_user = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'phone',
            'description',
            'address',
            'picture',
            'user',
            'email',
            'password',
            'create_user',
        )
    

    def save(self, *args, **kwargs):
        """
        Save a company.
        """
        if self.validated_data.get('create_user'):
            # Create user
            company_user = User.objects.create(
                email=self.validated_data.get('email'),
                username=self.validated_data.get('name'),
                password= make_password(self.validated_data.get('password')),
                picture=self.validated_data.get('picture', None),
                is_default_password=False,
                role='admin'
            )
            # Add user to validated data
            self.validated_data['user'] = company_user
            # Create company
            company = Company.objects.create(
                name=self.validated_data.get('name'),
                phone=self.validated_data.get('phone'),
                description=self.validated_data.get('description'),
                address=self.validated_data.get('address'),
                user=company_user
            )
            company.picture = self.validated_data.get('picture', None)
            company.save()
            return company
        
        return super().save(*args, **kwargs)

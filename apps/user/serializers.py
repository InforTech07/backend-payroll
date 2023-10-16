"""Users serializers."""
# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from apps.user.models import User
from apps.company.models import Company

# Serializers
#from apps.company.serializers import CompanySerializer
from apps.company.serializers import CompanySerializer

# libs
#from jwt
from datetime import timedelta



class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""
    # company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    ##obtener el objeto de la compañia
    #company = CompanySerializer(read_only=True)
    #employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True, default=None, read_only=True)
    #password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    company = CompanySerializer(read_only=True)
    class Meta:
        """Meta class."""
        model = User
        fields = (
            'id',
            'username',
            'email',
            'picture',
            'role',
            'is_default_password',
            'password',
            'company',
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer."""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    #company = CompanySerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'id',
            'username',
            'email',
            'picture',
            'role',
            'is_default_password',
            'company',
        )

    def validate(self, data):
        """Validate data."""
        print(data['email'])
        print(data['password'])
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Incorrect email or password')
        if user.is_default_password:
            raise serializers.ValidationError('User is in reset password')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve user."""
        #user = User.objects.get(email=self.context['email'])
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key



    # def create(self, data):
    #     """Generate or retrieve user."""
    #     user = User.objects.get(email=self.context['email'])
    #     token, created = Token.objects.get_or_create(user=user)
    #     return self.context['user'], token.key




    # def gen_reset_passwd_token(self, user):
    #     """Generate token reset passwd."""
    #     exp_date = timezone.now() + timedelta(days=1)
    #     payload = {
    #         'user': user,
    #         'exp': int(exp_date.timestamp()),
    #         'type': 'reset_password'
    #     }
    #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    #     return token


# class UserCreateSerializer(serializers.Serializer):
#     """Create New User serializer."""
#     username = serializers.CharField(min_length=4, max_length=20)
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
    
#     role = serializers.CharField(default='user')
#     password = serializers.CharField(
#         min_length=8, max_length=64, default='password')

#     def create(self, data):
#         """Create and return a new user."""
#         user = User.objects.create_user(**data)
#         return user
    
#     def save(self):
#         """Create and return a new user."""
#         user = User.objects.create_user(**self.validated_data)
#         return user


# class UserExistAccountSerializer(serializers.ModelSerializer):
#     """User ExistAccount serializer."""
#     class Meta:
#         """Meta class."""
#         model = User
#         fields = '__all__'


# class UserLoginSerializer(serializers.Serializer):
#     """User login serializer."""
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=8, max_length=128)

#     def validate(self, data):
#         """Validate data."""
#         print(data['email'])
#         print(data['password'])
#         user = authenticate(username=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError('Incorrect email or password')
#         if user.is_dafault_password:
#             raise serializers.ValidationError('User is in reset password')

#         self.context['user'] = user
#         return data

#     def create(self, data):
#         """Generate or retrieve user."""
#         token, created = Token.objects.get_or_create(user=self.context['user'])
#         return self.context['user'], token.key

    # def gen_reset_passwd_token(self, user):
    #     """Generate token reset passwd."""
    #     exp_date = timezone.now() + timedelta(days=1)
    #     payload = {
    #         'user': user,
    #         'exp': int(exp_date.timestamp()),
    #         'type': 'reset_password'
    #     }
    #     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    #     return token


# class UserResetPasswordSerializer(serializers.Serializer):
#     """User reset password serializer."""
#     password = serializers.CharField(min_length=8, max_length=128)
#     password_confirmation = serializers.CharField(min_length=8, max_length=128)

#     def validate(self, data):
#         """Validate data."""
#         passwd = data['password']
#         passwd_conf = data['password_confirmation']
#         if passwd != passwd_conf:
#             raise serializers.ValidationError('Passwords do not match')
#         password_validation.validate_password(passwd)
#         return data

#     def save(self, data):
#         """Update user's verified status."""
#         user = User.objects.get(email=data.get('email'))
#         user.set_password(self.validated_data['password'])
#         user.is_dafault_password = False
#         print('reset_)password')
#         user.save()
#         return user


# class UserVerifySerializer(serializers.Serializer):
#     #token = serializers.CharField()
#     password = serializers.CharField(min_length=8, max_length=128)
#     password_confirmation = serializers.CharField(min_length=8, max_length=128)

#     def validate(self, data):
#         """Validate data."""
#         passwd = data['password']
#         passwd_conf = data['password_confirmation']
#         if passwd != passwd_conf:
#             raise serializers.ValidationError('Passwords do not match')
#         password_validation.validate_password(passwd)
#         return data

    # def validate_token(self, data):
    #     """Validate token."""
    #     try:
    #         payload = jwt.decode(data, settings.SECRET_KEY,
    #                              algorithms=['HS256'])
    #     except jwt.ExpiredSignatureError:
    #         raise serializers.ValidationError('Verification link has expired')
    #     except jwt.PyJWTError:
    #         raise serializers.ValidationError('Invalid token')
    #     if payload['type'] != 'email_confirmation':
    #         raise serializers.ValidationError('Invalid token')
    #     self.context['payload'] = payload
    #     return data

    # def save(self):
    #     """Update user's verified status."""
    #     payload = self.context['payload']
    #     user = User.objects.get(username=payload['user'])
    #     user.set_password(self.validated_data['password'])
    #     user.is_verified = True
    #     user.is_dafault_password = False
    #     user.save()
    #     return user

from rest_framework import serializers
from datetime import date
from .models import StorePurchase
from apps.employee.models import Employee
from django.db.models import Sum

class StorePurchaseSerializer(serializers.ModelSerializer):
    """
    StorePurchase serializer.
    """
    date = serializers.DateField(read_only=True)
    company = serializers.IntegerField(read_only=True)
    class Meta:
        model = StorePurchase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def save(self, *args, **kwargs):
        """
        Save a store purchase.
        """
        date_now = date.today()
        base_salary = Employee.objects.get(id=self.validated_data['employee'].id).base_salary
        amount_credit = StorePurchase.objects.filter(cancelled=False, employee=self.validated_data['employee']).aggregate(Sum('total'))
        salary_available = 0
        if amount_credit['total__sum'] is None:
            salary_available = int(base_salary / 2 )
        else:
            salary_available = int(base_salary / 2 ) - amount_credit['total__sum']

        if salary_available > self.validated_data['total']:
            if date_now.day <= 18:
                store_purchase = StorePurchase.objects.create(
                    date=date_now,
                    total=self.validated_data['total'],
                    employee=self.validated_data['employee']
                )
                store_purchase.save()
                return store_purchase
            else:
                print('procede credito mayor a 15')
                print(salary_available)
                return date_now
        else:
            print(salary_available)
            raise serializers.ValidationError({'error': 'No tiene suficiente credito disponible'})

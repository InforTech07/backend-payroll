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
    #company = serializers.IntegerField(read_only=True)
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    class Meta:
        model = StorePurchase
        fields = ('id', 'date', 'total', 'cancelled', 'employee', 'company','biweekly', 'employee_name')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def save(self, *args, **kwargs):
        """
        Save a store purchase.
        """
        date_now = date.today()
        base_salary = Employee.objects.get(id=self.validated_data['employee'].id).base_salary
        amount_credit = StorePurchase.objects.filter(cancelled=False, employee=self.validated_data['employee']).aggregate(Sum('total'))
        salary_available = 0
        total_amount_credit = 0
        biweekly = False

        if date_now.day <= 15:
            salary_available = (float(base_salary) * 0.45) / 2
            biweekly = True
        else:
            salary_available = (float(base_salary) * 0.55) / 2

        
        if amount_credit['total__sum'] is None:
            total_amount_credit = float(self.validated_data['total'])
        else:
            total_amount_credit = float(amount_credit['total__sum']) + float(self.validated_data['total'])

        
        if salary_available > total_amount_credit:
            store_purchase = StorePurchase.objects.create(
                date=date_now,
                total=self.validated_data['total'],
                employee=self.validated_data['employee'],
                company=self.validated_data['company'],
                biweekly=biweekly
            )
            store_purchase.save()
            return store_purchase
        else:
            raise serializers.ValidationError({'error': 'No tiene suficiente credito disponible'})
        

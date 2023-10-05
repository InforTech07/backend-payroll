"""
    employee serializers
"""

from rest_framework import serializers

#models
from apps.company.models import Company
from apps.employee.models import (Department, 
                                  JobPosition, 
                                  Employee, 
                                  FamilyMember, 
                                  SalaryIncrease, 
                                  EmployeeDocument,
                                  Overtime,
                                  SalesCommission,
                                  ProductionBonus,
                                  )
from apps.payroll.models import (
    PayrollPeriod,
    Income,
)
from django.contrib.auth.hashers import make_password

from apps.user.models import User

#serializers
from apps.company.serializers import CompanySerializer
from apps.user.serializers import UserModelSerializer



class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the department model.
    """
    #company = CompanySerializer(read_only=True)

    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'description',
            'company',
        )

class JobPositionSerializer(serializers.ModelSerializer):
    """
    Serializer for the job position model.
    """
    # department = DepartmentSerializer(read_only=True)
    #   company = CompanySerializer(read_only=True)
    class Meta:
        model = JobPosition
        fields = (
            'id',
            'name',
            'description',
            'company',
        )

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the employee model.
    """
    email = serializers.EmailField(write_only=True, required=False)
    create_user = serializers.BooleanField(write_only=True, required=False)
    user = UserModelSerializer(read_only=True)
    job_position_name = serializers.CharField(source='job_position.name', read_only=True)
    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'address',
            'phone',
            'picture',
            'dpi',
            'birth_date',
            'date_hiring',
            'date_completion',
            'gender',
            'department',
            'base_salary',
            'base_salary_initial',
            'method_payment',
            'head_department',
            'job_position_name',
            'job_position', 
            'user',
            'company',
            'email',
            'create_user',
        )


    def save(self, *args, **kwargs):
        """
        Save a employee.
        """
        if self.validated_data.get('create_user'):
            # Create user
            employee_user = User.objects.create(
                email=self.validated_data.get('email'),
                username=self.validated_data.get('first_name') + self.validated_data.get('last_name'),
                password= make_password('@Password123'),
                picture=self.validated_data.get('picture', None),
                company=self.validated_data.get('company'),
                is_default_password=True,
                role='user'
            )
            # Add user to validated data
            self.validated_data['user'] = employee_user
            # Create company
            employee = Employee.objects.create(
                first_name=self.validated_data.get('first_name'),
                last_name=self.validated_data.get('last_name'),
                address=self.validated_data.get('address'),
                phone=self.validated_data.get('phone'),
                picture=self.validated_data.get('picture'),
                dpi=self.validated_data.get('dpi'),
                birth_date=self.validated_data.get('birth_date'),
                gender=self.validated_data.get('gender'),
                base_salary=self.validated_data.get('base_salary'),
                base_salary_initial=self.validated_data.get('base_salary'),
                method_payment=self.validated_data.get('method_payment'),
                head_department=self.validated_data.get('head_department'),
                department=self.validated_data.get('department'),
                date_hiring=self.validated_data.get('date_hiring'),
                date_completion=self.validated_data.get('date_completion'),
                job_position=self.validated_data.get('job_position'),
                user=employee_user,
                company=self.validated_data.get('company')
            )
            employee.save()
            return employee
        
        return super().save(*args, **kwargs)




class FamilyMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the family member model.
    """
    class Meta:
        model = FamilyMember
        fields = '__all__'

class SalaryIncreaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the salary increase model.
    """
    class Meta:
        model = SalaryIncrease
        fields = (
            'id',
            'amount',
            'reason',
            'employee',
        )
    
    def save(self, *args, **kwargs):
        """
        Save a salary increase.
        """
        employee = Employee.objects.get(id=self.validated_data.get('employee').id)

        salary_increase = SalaryIncrease.objects.create(
            reason=self.validated_data.get('reason'),
            amount=self.validated_data.get('amount'),
            employee=self.validated_data.get('employee')
        )
        salary_increase.save()
        employee.base_salary = employee.base_salary + salary_increase.amount
        employee.save()
        return salary_increase
    
class EmployeeDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the employee document model.
    """
    class Meta:
        model = EmployeeDocument
        fields = (
            'id',
            'name',
            'file',
            'employee',
        )

class OvertimeSerializer(serializers.ModelSerializer):
    """
    Serializaer for overtime employee
    """
    class Meta:
        model = Overtime
        fields = '__all__'


class SalesComissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the sales commission model.
    """
    class Meta:
        model = SalesCommission
        fields = '__all__'

    def save(self, *args, **kwargs):
        """
        Save a sales commission.
        • 0 – 100,000 en ventas 0.0%
        • 100,001 – 200,000 en ventas 2.5 %
        • 200,001 – 400,000 en ventas 3.5 %
        • 400,001 en adelante 4.5%
        """
        sales = self.validated_data.get('sales')
        current_commission = 0
        if int(sales) <= 100000:
            current_commission = 0
        elif int(sales) <= 200000:
            current_commission = int(sales) * 0.025
            print(current_commission)
        elif int(sales) <= 400000:
            current_commission = int(sales) * 0.035
        else:
            current_commission = int(sales) * 0.045
        sales_commission = SalesCommission.objects.create(
            sales=sales,
            commission=current_commission,
            employee=self.validated_data.get('employee')
        )
        sales_commission.save()
        return sales_commission
    
class ProductionBonusSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductionBonus
    cinco centavos por pieza elaborada
    """
    class Meta:
        model = ProductionBonus
        fields = '__all__'
    
    def save(self, *args, **kwargs):
        production = self.validated_data.get('production')
        current_bonus = int(production) * 0.05
        production_bonus = ProductionBonus.objects.create(
            production=production,
            bonus=current_bonus,
            employee=self.validated_data.get('employee')
        )
        production_bonus.save()
        return production_bonus
    



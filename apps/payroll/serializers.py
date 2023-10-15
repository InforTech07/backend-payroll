from datetime import date
from rest_framework import serializers
from apps.employee.models import Employee
from apps.payroll.models import (
    PayrollPeriod,
    Payroll,
    PayrollDeduction,
    PayrollIncome,
    PayrollAccountingTransaction,
    PayrollConcept,
)


class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = '__all__'



class PayrollSerializer(serializers.ModelSerializer):
    incomes = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    salary_base = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    social_insurance_employee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    social_insurance_company = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    employee_name = serializers.CharField(read_only=True)
    class Meta:
        model = Payroll
        fields = '__all__'

class PayrollDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollDeduction
        fields = '__all__'


class PayrollIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollIncome
        fields = '__all__'

class PayrollAccountingTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollAccountingTransaction
        fields = '__all__'
    
class PayrollConceptSerializer(serializers.ModelSerializer):
    """
    Serializer for the payroll concept model.
    """
    class Meta:
        model = PayrollConcept
        fields = '__all__'

    def save(self, *args, **kwargs):
        """
        Save a payroll concept.
        """
        concept = self.validated_data.get('concept')
        
        if concept is None:
            raise serializers.ValidationError('No existe un concepto de planilla')
        
        if concept == 'OVERTIME':
            return self.save_overtime()
        if concept == 'SALES_COMMISSION':
            return self.save_sales_commission()
        if concept == 'PRODUCTION_BONUS':
            return self.save_production_bonus()
        if concept == 'SOLIDARITY_CONTRIBUTION':
            return self.save_solidarity_contribution()
        if concept == 'LOANS':
            return self.save_loans()
        
        raise serializers.ValidationError('No existe un concepto de planilla')
        
    def save_overtime(self):
        """
        Save a overtime concept.
        """
        overtime_minutes = self.validated_data.get('overtime_minutes')
        public_holiday = self.validated_data.get('public_holiday')
        base_salary = Employee.objects.get(id=self.validated_data.get('employee').id).base_salary

        salary_per_hour = base_salary / 240
        amount_over_time = 0
        overtime_per_hour = int(overtime_minutes) / 60

        if public_holiday and int(overtime_minutes) > 30:
            amount_over_time = (overtime_per_hour * 4) * float(salary_per_hour)
        elif int(overtime_minutes) > 30:
            amount_over_time = (overtime_per_hour * 2) * float(salary_per_hour)

        payroll_concept = PayrollConcept.objects.create(
            concept='OVERTIME',
            employee=self.validated_data.get('employee'),
            payroll_period=self.validated_data.get('payroll_period'),
            company=self.validated_data.get('company'),
            reason=self.validated_data.get('reason'),
            overtime_minutes=overtime_per_hour,
            public_holiday=public_holiday,
            sales = 0,
            production = 0,
            amount=amount_over_time,
        )
        
        payrool_income = PayrollIncome.objects.create(
            employee=self.validated_data.get('employee'),
            type_concept='INGRESO',
            quantity=overtime_per_hour,
            amount=salary_per_hour,
            reason="Horas extras",
            total=amount_over_time,
            date=date.today(),
            payroll_period=self.validated_data.get('payroll_period'),
        )

        payroll_concept.save()
        payrool_income.save()
        return payroll_concept
    
    def save_sales_commission(self):
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
        payroll_concept = PayrollConcept.objects.create(
            concept='SALES_COMMISSION',
            employee=self.validated_data.get('employee'),
            payroll_period=self.validated_data.get('payroll_period'),
            reason=self.validated_data.get('reason'),
            overtime_minutes=0,
            public_holiday=False,
            sales = sales,
            production = 0,
            amount=current_commission,
            company=self.validated_data.get('company'),
        )

        payrool_income = PayrollIncome.objects.create(
            employee=self.validated_data.get('employee'),
            type_concept='INGRESO',
            quantity=1,
            amount=current_commission,
            total=current_commission * 1,
            reason="Comisiones de ventas",
            date=date.today(),
            payroll_period=self.validated_data.get('payroll_period'),
        )

        payroll_concept.save()
        payrool_income.save()
        return payroll_concept
    
    def save_production_bonus(self):
        """
        Save a production bonus.
        cinco centavos por pieza elaborada
        """
        production = self.validated_data.get('production')
        current_bonus = int(production) * 0.05
        payroll_concept = PayrollConcept.objects.create(
            concept='PRODUCTION_BONUS',
            employee=self.validated_data.get('employee'),
            payroll_period=self.validated_data.get('payroll_period'),
            reason=self.validated_data.get('reason'),
            overtime_minutes=0,
            public_holiday=False,
            sales = 0,
            production = production,
            amount=current_bonus,
            company=self.validated_data.get('company'),
        )

        payrool_income = PayrollIncome.objects.create(
            employee=self.validated_data.get('employee'),
            type_concept='INGRESO',
            quantity=self.validated_data.get('production'),
            amount=0.05,
            total=current_bonus,
            reason="Bonos de produccion",
            date=date.today(),
            payroll_period=self.validated_data.get('payroll_period'),
        )

        payroll_concept.save()
        payrool_income.save()
        return payroll_concept
    
    def save_solidarity_contribution(self):
        """
        Save a solidarity contribution.
        """
        payroll_concept = PayrollConcept.objects.create(
            concept='SOLIDARITY_CONTRIBUTION',
            employee=self.validated_data.get('employee'),
            payroll_period=self.validated_data.get('payroll_period'),
            reason=self.validated_data.get('reason'),
            overtime_minutes=0,
            public_holiday=False,
            sales = 0,
            production = 0,
            amount=self.validated_data.get('amount'),
            company=self.validated_data.get('company'),
        )

        payrool_deduction = PayrollDeduction.objects.create(
            employee=self.validated_data.get('employee'),
            type_concept='DEDUCCION',
            quantity=1,
            amount=self.validated_data.get('amount'),
            total=self.validated_data.get('amount') * 1,
            reason="Aportes solidarios",
            date=date.today(),
            payroll_period=self.validated_data.get('payroll_period'),
        )
        
        payrool_deduction.save()
        payroll_concept.save()
        
        return payroll_concept
    
    def save_loans(self):
        """
        Save a loans.
        """
        payroll_concept = PayrollConcept.objects.create(
            concept='LOANS',
            employee=self.validated_data.get('employee'),
            payroll_period=self.validated_data.get('payroll_period'),
            reason=self.validated_data.get('reason'),
            overtime_minutes=0,
            public_holiday=False,
            sales = 0,
            production = 0,
            amount=self.validated_data.get('amount'),
            company=self.validated_data.get('company'),
        )

        payrool_deduction = PayrollDeduction.objects.create(
            employee=self.validated_data.get('employee'),
            type_concept='DEDUCCION',
            quantity=1,
            amount=self.validated_data.get('amount'),
            total=self.validated_data.get('amount') * 1,
            reason="Prestamos",
            date=date.today(),
            payroll_period=self.validated_data.get('payroll_period'),
        )
        
        payrool_deduction.save()
        payroll_concept.save()
        
        return payroll_concept
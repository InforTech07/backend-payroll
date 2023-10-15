from django.db import models

#models
from apps.company.models import Company

# Create your models here.
from apps.employee.models import Employee


class PayrollPeriod(models.Model):
    """
    PayrollPeriod model.
    """
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    TYPE_PAYROLL = (
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
        ('BONO14', 'Bono14'),
        ('AGUINALDO', 'Aguinaldo'),
    )
    type = models.CharField(max_length=255, choices=TYPE_PAYROLL)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_period_company')
    is_open = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name



class Payroll(models.Model):
    """
    Payroll model.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_company')
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='payroll_payroll_period')
    date_generated = models.DateField(auto_now_add=True) # fecha de generacion de la planilla
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_open = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.name


class PayrollDeduction(models.Model):
    """
    Deduction model.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='deduction_employee')
    TYPES_CONCEPTS = (
        ('INGRESO', 'Ingreso'),
        ('DEDUCCION', 'Deduccion'),
        ('TRANSACCION_CONTABLE', 'Transaccion_contable'),
    )
    type_concept = models.CharField(max_length=255, choices=TYPES_CONCEPTS)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='deduction_payroll_period')

    def __str__(self):
        return self.type_concept


class PayrollIncome(models.Model):
    """
    Income model.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='income_employee')
    TYPES_CONCEPT = (
        ('INGRESO', 'Ingreso'),
        ('DEDUCCION', 'Deduccion'),
        ('TRANSACCION_CONTABLE', 'Transaccion_contable'),
    )
    type_concept = models.CharField(max_length=255, choices=TYPES_CONCEPT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='income_payroll_period')
    def __str__(self):
        return self.type_concept


class PayrollAccountingTransaction(models.Model):
    """
    PayrollAccountingTransaction model.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='accounting_transaction_employee')
    TYPES_CONCEPT = (
        ('INGRESO', 'Ingreso'),
        ('DEDUCCION', 'Deduccion'),
        ('TRANSACCION_CONTABLE', 'Transaccion_contable'),
    )
    type_concept = models.CharField(max_length=255, choices=TYPES_CONCEPT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='accounting_transaction_payroll_period')
    def __str__(self):
        return self.type_concept

class TransferBank(models.Model):
    """
    Model for a transfer bank. TRANSFERENCIAS BANCARIAS
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='transfer_bank_employee')
    date = models.DateField()
    BANKS = (
        ('BANRURAL', 'Banrural'),
        ('BANCO_INDUSTRIAL', 'Banco Industrial'),
        ('BANCO_GYT', 'Banco G&T'),
        ('BANTRAB', 'Bantrab'),
    )
    bank = models.CharField(max_length=200, choices=BANKS)
    account_number = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='transfer_bank_payroll_period')
    def __str__(self):
        return self.reason


class TransferCash(models.Model):
    """
    Model for a transfer cash. TRANSFERENCIAS EFECTIVO
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='transfer_cash_employee')
    date = models.DateField()
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='transfer_cash_payroll_period')

    def __str__(self):
        return self.reason


class PayrollConcept(models.Model):
    """
    Model for concepts payroll. CONCEPTOS PLANILLA
    """
    CONCEPT=(
        ('OVERTIME', 'Horas Extras'),
        ('SALES_COMMISSION', 'Comisiones de Venta'),
        ('PRODUCTION_BONUS', 'Bonos de Produccion'),
        ('SOLIDARITY_CONTRIBUTION', 'Aportes Solidarios'),
        ('LOANS', 'Prestamos'),
    )
    concept = models.CharField(max_length=255, choices=CONCEPT)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_concept_employee')
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='payroll_concept_payroll_period')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_concept_company')
    date = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=255)
    overtime_minutes = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    public_holiday = models.BooleanField(default=False, blank=True, null=True)
    sales = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    production = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    is_cancelled = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
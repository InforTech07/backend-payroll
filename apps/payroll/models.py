from django.db import models

#models
from apps.company.models import Company

# Create your models here.
from apps.employee.models import Employee, Department

class PayrollBase(models.Model):
    """
    PayrollBase model.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PayrollPeriod(PayrollBase):
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

    def __str__(self):
        return self.name

class PayrollConcept(PayrollBase):
    """
    PayrollConcept model.
    """
    name = models.CharField(max_length=255) # sueldo, horas extras, bono14...
    TYPES_CONCEPT = (
        ('INGRESOS', 'Ingreso'),
        ('DEDUCCION', 'Deduccion'),
        ('TRANSACCION_CONTABLE', 'Transaccion_contable'),
    )
    type = models.CharField(max_length=255, choices=TYPES_CONCEPT) # ingreso, deduccion
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_concept_company')

    def __str__(self):
        return self.name



class Payroll(PayrollBase):
    """
    Payroll model.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_employee')
    PayrollPeriod = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE, related_name='payroll_payroll_period')
    data_generated = models.DateField() # fecha de generacion de la planilla
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status_payroll = models.BooleanField(default=False) # estado de la planilla, si ya fue pagada o no


    def __str__(self):
        return self.name


class Deduction(PayrollBase):
    """
    Deduction model.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='deduction_employee')
    concept = models.ForeignKey(PayrollConcept, on_delete=models.CASCADE, related_name='deduction_concept')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.name




class Income(PayrollBase):
    """
    Income model.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='income_employee')
    concept = models.ForeignKey(PayrollConcept, on_delete=models.CASCADE, related_name='income_concept')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    def __str__(self):
        return self.name

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
    reason = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason
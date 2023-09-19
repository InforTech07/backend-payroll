from django.db import models

#models
from apps.company.models import Company

# Create your models here.
from apps.employee.models import Employee
from apps.user.models import User

class PayrollBase(models.Model):
    """
    PayrollBase model.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Payroll(PayrollBase):
    """
    Payroll model.
    """
    month = models.IntegerField()
    year = models.IntegerField()
    type = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payroll_company')

    def __str__(self):
        return self.name

class PayrollEmployee(PayrollBase):
    """
    PayrollEmployee model.
    """
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='payroll_employee_payroll')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_employee_employee')
    def __str__(self):
        return self.name
    

class SalaryIncrease(PayrollBase):
    """
    SalaryIncrease model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    porcentage = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='salary_increase_company')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salary_increase_user')

    def __str__(self):
        return self.name



class Bonus(PayrollBase):
    """
    Bonus model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    porcentage = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='bonus_company')

    def __str__(self):
        return self.name
    
class Deduction(PayrollBase):
    """
    Deduction model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    porcentage = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class PayrollEmployeeDetail(PayrollBase):
    """
    PayrollEmployeeDetail model.
    """
    payroll_employee = models.ForeignKey(PayrollEmployee, on_delete=models.CASCADE, related_name='payroll_employee_detail_payroll_employee')
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE, related_name='payroll_employee_detail_bonus')
    deduction = models.ForeignKey(Deduction, on_delete=models.CASCADE, related_name='payroll_employee_detail_deduction')
    def __str__(self):
        return self.name
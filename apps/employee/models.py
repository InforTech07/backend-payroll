"""
employee models
"""
from django.db import models
from apps.user.models import User
from apps.company.models import Company
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Sum


class Department(models.Model):
    """
    Department model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='department_company')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + '-' + self.company.name



class JobPosition(models.Model):
    """
    JobPosition model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_position_company')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + '-' + self.company.name



class Employee(models.Model):
    """
    Model for an employee.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    picture = models.CharField(max_length=200, blank=True, null=True)
    dpi = models.CharField(max_length=255)
    date_hiring = models.DateField()
    date_completion = models.DateField(blank=True, null=True)
    birth_date = models.DateField()
    GENDERS = (
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
    )
    gender = models.CharField(max_length=10, choices=GENDERS)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    base_salary_initial = models.DecimalField(max_digits=10, decimal_places=2)
    head_department = models.BooleanField(default=False)
    METHOD_PAYMENTS = (
        ('EFECTIVO', 'Efectivo'),
        ('CHEQUE', 'Cheque'),
        ('TRANSFERENCIA', 'Transferencia'),
    )
    method_payment = models.CharField(max_length=255, choices=METHOD_PAYMENTS)
    BANKS = (
        ('BANRURAL', 'Banrural'),
        ('BANCO_INDUSTRIAL', 'Banco Industrial'),
        ('BANCO_GYT', 'Banco G&T'),
        ('BANTRAB', 'Bantrab'),
    )
    bank = models.CharField(max_length=255, blank=True, null=True, choices=BANKS)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee_department')
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='employee_job_position')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user', blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def calculte_payroll_monthly(self,payroll_period):
        """
        calculte salary.
        """
        social_insurance_employee = float(self.base_salary) * 0.0483
        social_insurance_company = float(self.base_salary) * 0.1067
        total_income = sum([income.total for income in self.income_employee.filter(payroll_period=payroll_period)])
        total_deduction = sum([deduction.total for deduction in self.deduction_employee.filter(payroll_period=payroll_period)])
        total_salary = float(self.base_salary) + float(total_income) - float(total_deduction) - float(social_insurance_employee)
        data = {
            'salary': self.base_salary,
            'total_income': total_income,
            'total_deduction': total_deduction,
            'social_insurance_employee': social_insurance_employee,
            'social_insurance_company': social_insurance_company,
            'total_salary': total_salary
        }
        return data


    def calculte_bono14(self):
        """
        Calculate bono14.
        """
        # obtenemos la fecha actual
        current_date = date.today()
        # tiempo de trabajado hasta la fecha actual
        time_worked = current_date.year - self.date_hiring.year

        # caculamos le total de salarios devengados
        previous_start_date = current_date.replace(year=current_date.year-1, month=1, day=1)
        previous_end_date = current_date - timedelta(days=1)

        accrued_salaries = self.payroll_employee.filter(
            payroll_period__start_date__range=[previous_start_date, previous_end_date],
            status_payroll='Pagada'
        ).aggregate(total=Sum('total'))['total']

        return bono14
    
    def calculate_aguinaldo(self):
        if self.hire_date.year == timezone.now().year:
            days_worked = (timezone.now() - self.hire_date).days
            aguinaldo = (self.salary / 365) * days_worked
        else:
            aguinaldo = (self.salary / 12)
        
        return aguinaldo
    
    def calculate_severance(self):
        if self.termination_date:
            years_worked = (self.termination_date - self.hire_date).days / 365
            severance_pay = self.salary * years_worked
            return severance_pay
        else:
            return 0
    
    def check_credit_available(self):
        if self.credit_available > 0:
            return True
        else:
            return False
    def get_employee_by_user(self, user):
        return Employee.objects.get(user=user)
        
class EmployeeDocument(models.Model):
    """
    Model for an employee document.
    """
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_document_employee')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class FamilyMember(models.Model):
    """
    Model for a family member.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255) # Parent, Son, Daughter, etc.
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='family_member_employee')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    
class SalaryIncrease(models.Model):
    """
    Model for a salary increase.
    """    
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_increase_employee')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason

class RequestAbsence(models.Model):
    """
    Model for a request absence. PERMISOS
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='request_absence_employee')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255)
    REQUEST_STATUS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('APROBADO_SIN_DESCUENTO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    )
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default='PENDIENTE')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='request_absence_company')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason



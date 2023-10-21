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
    
    def calculate_salary_biweekly(self, payroll_period):
        """
        Calculate salary biweekly.
        """
        date_hiring_instance = self.date_hiring
        start_date = payroll_period.start_date
        end_date = payroll_period.end_date

        days = (end_date - start_date).days
        salary_for_day = self.base_salary / days
        days_worked = (end_date - date_hiring_instance).days

        if date_hiring_instance > end_date:
            return 0
        elif date_hiring_instance < start_date:
            return float(self.base_salary) *  0.45
        else:
            return 0

    def calculate_bono14(self, payroll_period):
        """
        calculte bono14 employee.
        """
        base_salary = self.base_salary
        days_worked = (payroll_period.end_date - self.date_hiring).days
        if days_worked > 365:
            return base_salary
        else:
            return  float(base_salary) * float(days_worked) / 365
        

    def calculate_aguinaldo(self, payroll_period):
        """
        calculte aguinaldo employee.
        """
        base_salary = self.base_salary
        diff = (payroll_period.end_date.year - self.date_hiring.year) * 12 + (payroll_period.end_date.month - self.date_hiring.month)
        if diff > 12:
            return base_salary
        else:
            return float(base_salary) * float(diff) / 12


    def get_calculate_payroll(self, payroll_period):
        """
            calculte payroll employee.
        """
        if self.date_hiring > payroll_period.end_date:
            return{
                'gross_salary': 0,
                'net_salary': 0,
                'total_income': 0,
                'total_deduction': 0,
                'social_insurance_employee': 0,
                'social_insurance_company': 0,
                'gross_biweekly_salary': 0,
                'net_biweekly_salary': 0,
                'total_biweekly_deduction': 0,
                'bono14': 0,
                'aguinaldo': 0,
            }

        social_insurance_employee = float(self.base_salary) * 0.0483
        social_insurance_company = float(self.base_salary) * 0.1067
        bono14 = self.calculate_bono14(payroll_period)
        aguinaldo = self.calculate_aguinaldo(payroll_period)
        biweekly_salary = self.calculate_salary_biweekly(payroll_period)
        total_income = sum([income.total for income in self.income_employee.filter(payroll_period=payroll_period)])
        total_deduction = sum([deduction.total for deduction in self.deduction_employee.filter(payroll_period=payroll_period)])
        credit_store_biweekly = sum([store.total for store in self.store_purchase_employee.filter(cancelled=False, employee=self, biweekly=True)])
        credit_store = sum([store.total for store in self.store_purchase_employee.filter(cancelled=False, employee=self, biweekly=False)])
        total_biweekly_deduction = 0
        #permission = sum([permission.total for permission in self.request_absence_employee.filter(payroll_period=payroll_period, status='APROBADO')])
        if credit_store > 0:
            total_deduction = float(total_deduction) + float(credit_store)

        if credit_store_biweekly > 0:
            total_biweekly_deduction = float(total_biweekly_deduction) + float(credit_store_biweekly)

        gross_salary = float(self.base_salary) + float(total_income)
        net_salary = float(gross_salary) - float(total_deduction) - float(social_insurance_employee)

        gross_salary_biweekly = float(biweekly_salary) 
        net_salary_biweekly = float(biweekly_salary) - float(total_biweekly_deduction) 

        data = {
            'gross_salary': gross_salary,
            'net_salary': net_salary,
            'total_income': total_income,
            'total_deduction': total_deduction,
            'social_insurance_employee': social_insurance_employee,
            'social_insurance_company': social_insurance_company,
            'gross_biweekly_salary': gross_salary_biweekly,
            'net_biweekly_salary': net_salary_biweekly,
            'total_biweekly_deduction': total_biweekly_deduction,
            'bono14': bono14,
            'aguinaldo': aguinaldo,
        }

        return data
    
    
    
    
    
    def calculte_payroll_monthly(self,payroll_period):
        """
        calculte salary.
        """
        social_insurance_employee = float(self.base_salary) * 0.0483
        social_insurance_company = float(self.base_salary) * 0.1067
        total_income = sum([income.total for income in self.income_employee.filter(payroll_period=payroll_period)])
        total_deduction = sum([deduction.total for deduction in self.deduction_employee.filter(payroll_period=payroll_period)])
        credit_store = sum([store.total for store in self.store_purchase_employee.filter(cancelled=False, employee=self)])
        if credit_store > 0:
            total_deduction = float(total_deduction) + float(credit_store)
        
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

    def calculte_biweekly_payroll(self,payroll_period):
        """
        calculte salary.
        """
        salary = float(self.base_salary) * 0.45
        credit_store = sum([store.total for store in self.store_purchase_employee.filter(cancelled=False, employee=self)])
        total_salary = float(salary) - float(credit_store)

        data = {
            'salary': salary,
            'total_income': 0,
            'total_deduction': credit_store,
            'social_insurance_employee': 0,
            'social_insurance_company': 0,
            'total_salary': total_salary
        }
        return data

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='request_absence_company')
    date_request = models.DateField()
    reason = models.CharField(max_length=255)
    REQUEST_STATUS = (
        ('PENDIENTE', 'Pendiente'),
        ('APROBADO', 'Aprobado'),
        ('APROBADO_SIN_DESCUENTO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    )
    status = models.CharField(max_length=255, choices=REQUEST_STATUS, default='PENDIENTE')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason



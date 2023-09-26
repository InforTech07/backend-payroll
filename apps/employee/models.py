"""
employee models
"""
from django.db import models
from apps.user.models import User
from apps.company.models import Company
from datetime import date, timedelta

class EmployeeBase(models.Model):
    """
    EmployeeBase model.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Department(EmployeeBase):
    """
    Department model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    #head_department = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='department_company')

    def __str__(self):
        return self.name



class JobPosition(EmployeeBase):
    """
    JobPosition model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_position_company')
    def __str__(self):
        return self.name



class Employee(EmployeeBase):
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
    gender = models.CharField(max_length=10)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee_department')
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='employee_job_position')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company')

    def __str__(self):
        return self.first_name
    
    def calculte_total_salary(self):
        """
        Calculate total salary.
        """
        income_employee = sum([income.amount for income in self.income_employee.filter(is_active=True)])
        deduction_employee = sum([deduction.amount for deduction in self.deduction_employee.filter(is_active=True)])
        total_salary = self.base_salary + income_employee - deduction_employee
        return total_salary


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
    D
class EmployeeDocument(EmployeeBase):
    """
    Model for an employee document.
    """
    name = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_document_employee')

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
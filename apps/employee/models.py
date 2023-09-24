"""
employee models
"""
from django.db import models
from apps.user.models import User
from apps.company.models import Company
from apps.payroll.models import Deduction, Income

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
    head_department = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
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
    picture = models.CharField(max_length=200, blank=True, null=True)
    dpi = models.CharField(max_length=255)
    date_hiring = models.DateField()
    date_completion = models.DateField()
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
        # total_salary = self.base_salary
        # salary_increases = self.salary_increase_employee.filter(is_active=True)
        # for salary_increase in salary_increases:
        #     total_salary += salary_increase.amount
        # return total_salary
    
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
    picture = models.CharField(max_length=200, blank=True, null=True)
    kinship = models.CharField(max_length=255) # Parent, Son, Daughter, etc.
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
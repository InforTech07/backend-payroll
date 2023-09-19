"""
employee models
"""
from django.db import models
from apps.user.models import User
from apps.company.models import Company

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
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='department_company')

    def __str__(self):
        return self.name



class JobPosition(EmployeeBase):
    """
    JobPosition model.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
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
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    dpi_file = models.FileField(upload_to='employee_file', blank=True, null=True)
    degree_file = models.FileField(upload_to='employee_file', blank=True, null=True)
    criminal_record_file = models.FileField(upload_to='employee_file', blank=True, null=True)
    head_department = models.BooleanField(default=False)
    job_position = models.OneToOneField(JobPosition, on_delete=models.CASCADE, related_name='employee_job_position')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company')

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
        return self.name
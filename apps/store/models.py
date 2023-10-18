""" Store models"""
from django.db import models

# Create your models here.
from apps.employee.models import Employee
#from apps.company.models import Company

class StorePurchase(models.Model):
    """
    Model for a store purchase.
    """
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cancelled = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='store_purchase_employee')
    #company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='store_purchase_company')

    def __str__(self):
        return self.name



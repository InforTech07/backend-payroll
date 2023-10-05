""" Store models"""
from django.db import models

# Create your models here.
from apps.user.models import User
from apps.company.models import Company

class StoreBase(models.Model):
    """
    StoreBase model.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StorePurchase(StoreBase):
    """
    Model for a store purchase.
    """
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_purchase_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='store_purchase_company')

    def __str__(self):
        return self.name



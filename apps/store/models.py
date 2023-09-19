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


class Category(StoreBase):
    """
    Model for a category.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='category_company')

    def __str__(self):
        return self.name
    
class Product(StoreBase):
    """
    Model for a product.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    picture = models.CharField(max_length=200, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_company')

    def __str__(self):
        return self.name

class Order(StoreBase):
    """
    Model for a order.
    """
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='order_company')
    def __str__(self):
        return self.name
    

class Detail(StoreBase):
    """
    Model for a detail.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='detail_product')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='detail_order')
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Sale(StoreBase):
    """
    Model for a sales.
    """
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sales_company')
    def __str__(self):
        return self.name
    

class CreditStore(StoreBase):
    """
    Model for a credit store.
    """
    date = models.DateField()
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_store_user')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='credit_store_company')
    def __str__(self):
        return self.name
""" 
Models for the company app.
"""

from django.db import models

class Company(models.Model):
    """
    Model for a company.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    picture = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.name
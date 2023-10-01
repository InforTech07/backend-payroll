from django.db import models

# Create your models here.
# media models
# utils
from django.db import models
from datetime import datetime


def nameFile(instance, filename):
    today_data = datetime.now()
    extension = "." + filename.split(".")[-1]
    return '/'.join(['img', str(today_data.year), str(today_data.month), str(today_data.day), str(today_data.hour), str(today_data.minute), str(today_data.second) + extension])

# Create your models here.

class MediaBase(models.Model):
    """
    EmployeeBase model.
    """
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PayrollImage(MediaBase):
    picture = models.ImageField(upload_to='images')

    def __str__(self):
        return "Image at " + str(self.created_at)
    

class PayrollFile(MediaBase):
    file = models.FileField(upload_to='files')

    def __str__(self):
        return "File at " + str(self.created_at)
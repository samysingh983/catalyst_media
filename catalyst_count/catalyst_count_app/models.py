from django.contrib.auth.models import AbstractUser
from django.db import models

class CatalystUser(AbstractUser):
    email = models.EmailField(unique=True)

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, default='Pending')

class Data(models.Model):
    name = models.TextField(null=True)
    domain = models.TextField(null=True)
    year_founded = models.CharField(max_length=10,null=True)
    industry = models.TextField(null=True)
    size_range = models.TextField(null=True)
    locality = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    linkedin_url = models.TextField(null=True)
    current_employee_estimate = models.IntegerField(null=True)
    total_employee_estimate = models.IntegerField(null=True)
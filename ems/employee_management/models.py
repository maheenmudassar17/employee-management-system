# employee_management/models.py

from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


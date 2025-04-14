# employee_management/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    

    


# employee_management/models.py

# models.py

class Task(models.Model):
    name = models.CharField(max_length=255, default='Untitled Task')
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Task {self.id}"  # Or another field to represent the task


from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_filter = ('status',)  # This will allow filtering by status

admin.site.register(Task, TaskAdmin)

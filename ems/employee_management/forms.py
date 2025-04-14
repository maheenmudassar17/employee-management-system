# employee_management/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Employee

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['designation', 'salary']


# employee_management/forms.py

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name','description', 'assigned_to', 'status']  # Only include fields that are defined in the model

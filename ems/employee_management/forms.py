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

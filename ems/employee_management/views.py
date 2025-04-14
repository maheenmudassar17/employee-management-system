# employee_management/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserForm, EmployeeForm
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import redirect




def superuser_only(user):
    return user.is_superuser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('employee_portal')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def admin_dashboard(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def add_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        emp_form = EmployeeForm(request.POST)
        if user_form.is_valid() and emp_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('employee_list')
    else:
        user_form = UserForm()
        emp_form = EmployeeForm()
    return render(request, 'employee_form.html', {'user_form': user_form, 'emp_form': emp_form})


def employee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect('employee_portal')
        else:
            messages.error(request, 'Invalid credentials or you are not an employee.')

    return render(request, 'employee_login.html')

@login_required(login_url='/employee-login/')
def employee_portal(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'employee_portal.html')

# employee_management/views.py
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import TaskForm, UserForm, EmployeeForm
from .models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from .models import Task
from django.db.models import Q






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
    employees = Employee.objects.all()
    return render(request, 'admin_dashboard.html', {'employees': employees})

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
            user = user_form.save()
            employee = emp_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('employee_list')  # or wherever you want to redirect
    else:
        user_form = UserForm()
        emp_form = EmployeeForm()

    # Add custom CSS classes to form fields
    user_form.fields['username'].widget.attrs.update({'class': 'form-control'})
    user_form.fields['email'].widget.attrs.update({'class': 'form-control'})
    user_form.fields['password'].widget.attrs.update({'class': 'form-control'})
    
    emp_form.fields['designation'].widget.attrs.update({'class': 'form-control'})
    emp_form.fields['salary'].widget.attrs.update({'class': 'form-control'})

    return render(request, 'employee_form.html', {
        'user_form': user_form,
        'emp_form': emp_form
    })
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
@login_required(login_url='/employee-login/')
def employee_portal(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    employee = get_object_or_404(Employee, user=request.user)
    tasks = Task.objects.filter(assigned_to=employee).order_by('-id')

    return render(request, 'employee_portal.html', {'tasks': tasks})



@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'assign_task.html', {'form': form})

@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def edit_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    user = employee.user

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']
        user.save()

        employee.designation = request.POST['designation']
        employee.salary = request.POST['salary']
        employee.save()

        return redirect('admin_dashboard')

    return render(request, 'edit_employee.html', {'employee': employee})
    

@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    employee.user.delete()  # This also deletes the related employee
    return redirect('admin_dashboard')



@login_required
def employee_task_list(request):
    employee = Employee.objects.get(user=request.user)
    tasks = Task.objects.filter(assigned_to=employee)
    return render(request, 'employee_tasks.html', {'tasks': tasks})


# views.py

from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

@require_POST
@login_required
def mark_task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.assigned_to.user == request.user:
        task.status = 'Completed'
        task.save()
    return redirect('employee_tasks')

@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def add_task(request):
    # Get the list of employees to populate the dropdown
    employees = Employee.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Process form data
            form.save()

    return render(request, 'assign_task.html', {
        'form': form,
        'employees': employees  # Pass the list of employees to the template
    })


@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # or your target page
    else:
        form = TaskForm(instance=task)

    # 👇 Fetch all employees for the dropdown
    employees = Employee.objects.all()

    # 👇 Send form, task, and employees to the template
    return render(request, 'edit_task.html', {
        'form': form,
        'task': task,
        'employees': employees,
    })
@login_required(login_url='/')
@user_passes_test(superuser_only, login_url='/')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def custom_login(request):
    # login logic
    if request.user.is_authenticated:
        return redirect('employee_task_list')  # Redirect to the employee task list page


def admin_dashboard(request):
    query = request.GET.get('q')
    if query:
        employees = Employee.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(designation__icontains=query)
        )
    else:
        employees = Employee.objects.all()
    return render(request, 'admin_dashboard.html', {'employees': employees})



def task_list(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(name__icontains=query) |
            Q(assigned_to__user__first_name__icontains=query) |
            Q(assigned_to__user__last_name__icontains=query)
        )
    else:
        tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

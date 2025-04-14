# employee_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employee-login/', views.employee_login, name='employee_login'),
    path('employee-portal/', views.employee_portal, name='employee_portal'),
]


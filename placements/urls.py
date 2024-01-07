from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_db',views.admin_db,name='admin_db'),
    path('login',views.login1,name='login'),
    path('update_status',views.update_status,name='update_status'),
    path('add_job',views.add_job,name='add_job'),
    path('job_vacancy',views.job_vacancy,name='job_vacancy'),
    path('registration',views.registration,name='registration'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('company_logout',views.company_logout,name='company_logout'),
    path('company_details',views.add_company_details,name='company_details'),
    path('company_dashboard',views.company_dashboard,name="company_dashboard"),
    path('search_results',views.search_results,name='search_results'),
    path('user_registration',views.user_registration,name='user_registration'),
    path('user_login',views.user_login,name='user_login'),
    ]

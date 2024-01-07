from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_db',views.admin_db,name='admin_db'),
    path('login',views.login1,name='login'),
    path('top_companies',views.top_companies,name='top_companies'),
    path('update_status',views.update_status,name='update_status'),
    path('add_job',views.add_job,name='add_job'),
    path('job_vacancy',views.job_vacancy,name='job_vacancy'),
    path('registration',views.registration,name='registration'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('company_logout',views.company_logout,name='company_logout'),
    path('company_details',views.add_company_details,name='company_details'),
    path('add_top_company',views.add_top_company,name='add_top_company'),
    path('company_dashboard',views.company_dashboard,name="company_dashboard"),
    path('add_questions',views.add_questions,name="add_questions"),
    path('company_dashboard',views.company_dashboard,name="company_dashboard"),
    path('search_results',views.search_results,name='search_results'),
    path('user_registration',views.user_registration,name='user_registration'),
    path('user_login',views.user_login,name='user_login'),
    path('search_trend/<str:keyword>/', views.search_trend, name='search_trend'),
    path('single_job/<int:job_id>',views.single_job,name='single_job'),
    path('company/<int:id>',views.company,name='company'),
    path('job_list/<str:department>',views.job_list,name='job_list'),
    path('all_companies',views.all_companies,name='all_companies'),
    path('all_jobs',views.all_jobs,name='all_jobs'),
    path('work_mode/<str:selected_work_mode>/', views.work_mode, name='work_mode'),
    path('location_related_jobs/<str:location>',views.location_related_jobs,name='location_related_jobs'),
    path('autocomplete-job-title/', views.autocomplete_job_title_suggestions, name='autocomplete_job_title'),
    
    ]

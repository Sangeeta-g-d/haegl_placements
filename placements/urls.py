from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('upload_file',views.upload_file,name='upload_file'),
    path('new_index',views.new_index,name='new_index'),
    path('contact_us',views.contact_us,name='contact_us'),
    path('temp1',views.temp1,name='temp1'),
    path('temp3',views.temp3,name='temp3'),
    path('temp2',views.temp2,name='temp2'),
    path('select_theme',views.select_theme,name='select_theme'),
    path('internship_program',views.internship_program,name='internship_program'),
    path('new_user_register',views.new_user_register,name='new_user_register'),
    path('new_job_des/<int:id>',views.new_job_des,name='new_job_des'),
    path('display_uploaded_file', views.display_uploaded_file, name='display_uploaded_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
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
    path('user_details',views.user_details,name="user_details"),
    path('user_job_list/<str:department>',views.user_job_list,name="user_job_list"),
    path('search_results',views.search_results,name='search_results'),
    path('internship_search_results',views.internship_search_results,name='internship_search_results'),
    path('internship_search',views.internship_search,name='internship_search'),
    path('user_search_results',views.user_search_results,name='user_search_results'),
    path('user_registration',views.user_registration,name='user_registration'),
    path('user_login',views.user_login,name='user_login'),
    path('search_trend/<str:keyword>/', views.search_trend, name='search_trend'),
    path('single_job/<int:job_id>',views.single_job,name='single_job'),
    path('user_single_job/<int:job_id>',views.user_single_job,name='user_single_job'),
    path('company/<int:id>',views.company,name='company'),
    path('job_list/<str:department>',views.job_list,name='job_list'),
    path('all_companies',views.all_companies,name='all_companies'),
    path('all_jobs',views.all_jobs,name='all_jobs'),
    path('work_mode/<str:selected_work_mode>/', views.work_mode, name='work_mode'),
    path('user_work_mode/<str:selected_work_mode>/', views.user_work_mode, name='user_work_mode'),
    path('location_related_jobs/<str:location>',views.location_related_jobs,name='location_related_jobs'),
    path('user_location_related/<str:location>',views.user_location_related,name='user_location_related'),
    path('autocomplete-job-title/', views.autocomplete_job_title_suggestions, name='autocomplete_job_title'),
    path('autocomplete-internship-title/', views.autocomplete_internship_title_suggestions, name='autocomplete_internship_title'),
    path('questions/<int:id>', views.questions, name='questions'),
    path('user_dashboard',views.user_dashboard1,name='user_dashboard'),
    path('application/<int:job_id>',views.application,name="application"),
    path('saved_jobs',views.saved_jobs,name='saved_jobs'),
    path('job_applications',views.job_applications,name='job_applications'),
    path('jobs',views.jobs,name='jobs'),
    path('save_job/<int:job_id>/<int:u_id>/',views.save_job,name="save_job"),
    path('remove_job/<int:job_id>/<int:u_id>/',views.remove_job,name="remove_job"),
    path('delete_application/<int:pk>',views.delete_application,name="delete_application"),
    path('profile',views.profile,name='profile'),
    path('internships',views.internships,name='internships'),
    path('internship_list',views.internship_list,name='internship_list'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('companies',views.companies,name='companies'),
    path('add_internship',views.add_internship,name='add_internship'),
    path('user_internship',views.user_internship,name='user_internship'),
    path('application_status',views.application_status,name='application_status'),
    path('company_info/<int:id>',views.company_info,name='company_info'),
    path('toggle_status/<int:job_id>/', views.toggle_status, name='toggle_status'),
    path('designation_questions/', views.designation_questions, name='designation_questions'),
    path('new_all_jobs',views.new_all_jobs,name='new_all_jobs'),
    path('temp4',views.temp4,name='temp4'),
    path('pic',views.pic,name='pic'),


]

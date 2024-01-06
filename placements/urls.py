from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [

    path('admin_db',views.admin_db,name='admin_db'),
    path('login',views.login,name='login'),
    path('registration',views.registration,name='registration'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),

    ]

from django.contrib import admin
from django.urls import path
from . import views
from .views import home, redirect_signin, redirect_signup, postsignup, postsignin, redirect_job_creation, redirect_admin, redirect_profile

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signin/', views.redirect_signin, name='signin'), 
    path('signup/', views.redirect_signup, name='signup'),
    path('admin/', admin.site.urls), 
    path('postsignup/', views.postsignup, name='postsignup'),
    path('postsignin/', views.postsignin, name='postsignin'),
    path('job_creation/', views.redirect_job_creation, name='job_creation'),
    path('create_job/', views.create_job, name='create_job'),
    path('adminpage/', views.redirect_admin, name='adminpage'),
    path('delete/', views.accountDelete, name='delete')
    path('profile/', views.redirect_profile, name='profile')
]


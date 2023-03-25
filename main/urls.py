from django.contrib import admin
from django.urls import path
from . import views
<<<<<<< HEAD
from .views import home, redirect_signin, redirect_signup, postsignup, postsignin, redirect_job_creation, redirect_admin, jobview, logout, applytojob
=======
from .views import home, redirect_signin, redirect_signup, postsignup, postsignin, redirect_job_creation, redirect_admin, redirect_profile
>>>>>>> dcdcc6571c2f5fd9dbf11b99f98fd53375545758

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signin/', views.redirect_signin, name='signin'), 
    path('signup/', views.redirect_signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('admin/', admin.site.urls), 
    path('postsignup/', views.postsignup, name='postsignup'),
    path('postsignin/', views.postsignin, name='postsignin'),
    path('job_creation/', views.redirect_job_creation, name='job_creation'),
    path('create_job/', views.create_job, name='create_job'),
<<<<<<< HEAD
    path('jobview/', views.jobview, name='jobview'),
    path('applytojob/', views.applytojob, name='applytojob'),
    path('adminpage/', views.redirect_admin, name='adminpage')
=======
    path('adminpage/', views.redirect_admin, name='adminpage'),
    path('profile/', views.redirect_profile, name='profile')
>>>>>>> dcdcc6571c2f5fd9dbf11b99f98fd53375545758
]


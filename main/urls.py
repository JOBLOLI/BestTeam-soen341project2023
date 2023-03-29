from django.contrib import admin
from django.urls import path
from . import views
from .views import home, redirect_signin, redirect_signup, redirect_edit_profile, edit_profile, postsignup, postsignin, redirect_job_creation, create_job, redirect_admin, jobview, logout, applytojob, redirect_profile, jobmanage, accept, decline, profileview, edit_profile

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
    path('jobview/', views.jobview, name='jobview'),
    path('jobmanage/', views.jobmanage, name='jobmanage'),
    path('jobmanage/accept/', views.accept, name='accept'),
    path('jobmanage/decline/', views.decline, name='decline'),
    path('applytojob/', views.applytojob, name='applytojob'),
    path('adminpage/', views.redirect_admin, name='adminpage'),
    path('profile/', views.redirect_profile, name='profile'),
    path('profileview/', views.profileview, name='profileview'),
    path('profileview/redirect_edit_profile/', views.redirect_edit_profile, name='redirect_edit_profile'),
    path('', views.edit_profile, name='edit_profile'),
]

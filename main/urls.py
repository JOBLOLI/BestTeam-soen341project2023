from django.contrib import admin
from django.urls import path
from . import views
from .views import home, redirect_signin, redirect_signup, postsignup, postsignin

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signin/', views.redirect_signin, name='signin'), 
    path('signup/', views.redirect_signup, name='signup'),
    path('admin/', admin.site.urls), 
    path('postsignup/', views.postsignup, name='postsignup'),
    path('postsignin/', views.postsignin, name='postsignin')
]


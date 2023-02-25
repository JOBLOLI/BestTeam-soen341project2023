from django.urls import path
from . import views
from .views import cringe, redirect_signin

urlpatterns = [
    path('', views.cringe, name='homepage'),
    path('redirect/', views.redirect_signin, name='signin'),   
]

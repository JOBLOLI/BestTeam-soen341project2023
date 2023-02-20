from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
path("", views.index, name= "index"),
path("admin/", admin.site.urls),
path("postsignIn/", views.postsignIn),
path("signUp/", views.signUp, name="signup"),
path("logout/", views.logout, name="log"),
path("postsignUp/", views.postsignUp),
]
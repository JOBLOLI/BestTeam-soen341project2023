from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

config={
    "apiKey": "AIzaSyAim4TyliA_tnns9WFI1y5eQBdlMrQm58Q",
    "authDomain": "djangoproject-620c6.firebaseapp.com",
    "databaseURL":"https://djangoproject-620c6-default-rtdb.firebaseio.com/",
    "projectId": "djangoproject-620c6",
    "storageBucket": "djangoproject-620c6.appspot.com",
    "messagingSenderId": "645132885500",
    "appId": "1:645132885500:web:7ffb3a5d868b6c53816679",
}

firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def cringe(request):
    context = {'foo': 'bar'}
    return render(request, 'home.html', context)

def redirect_signin(request):
    return render(request,'signin.html')


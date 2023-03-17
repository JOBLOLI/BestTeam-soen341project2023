from django.shortcuts import render, redirect
from django.contrib import messages
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
auth=firebase.auth()
database=firebase.database()

def home(request):
    context = {'foo': 'bar'}
    return render(request, 'home.html', context)

def redirect_signin(request):
    return render(request,'signin.html')

def redirect_signup(request):
    return render(request, 'signup.html')

def redirect_delete(request):
    return render(request, 'delete.html')

# signin and signup options
def postsignup(request):
    email = request.POST.get('email')
    pasw = request.POST.get('password1')
    try:
        user = auth.create_user_with_email_and_password(email,pasw)
        uid = user['localId']
        idtoken = request.session['uid']
        print(uid)
    except:
        message = "Email already in use"
        return render(request, "signin.html",{"message":message})
    return render(request,"home.html")

def postsignin(request):
    email = request.POST.get('email')
    pasw = request.POST.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email,pasw)
    except:
        message = "Invalid Credentials"
        return render(request,"signin.html",{"message":message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request,"home.html",{"email":email})


def accountDeletion(request):
    """ Deletes account of currently logged in user"""
    user = auth.current_user['localId']
    auth.delete_user_account(user['idToken'])
    return render(request, 'home.html')
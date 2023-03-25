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
    jobs = database.child("jobs").get()
    for job in jobs.each():
        print(job.val())
    context = {"jobs":jobs.val()}
    return render(request, 'home.html', context)

def redirect_signin(request):
    return render(request,'signin.html')

def redirect_signup(request):
    return render(request, 'signup.html')

def redirect_job_creation(request):
    # Check if user is signed in and is an employer
    if 'uid' in request.session and request.session['user_type'] == 'employer':
        return render(request, 'job_creation.html')
    else:
        return redirect('/signin/')
    
def redirect_admin(request):
    # Check if user is signed in and is an employer
    if 'uid' in request.session and request.session['user_type'] == 'admin':
        return render(request, 'admin_p.html')
    else:
        return redirect('/signin/')
        
def create_job(request):
    if request.method == 'POST':
    # Get form data
        jobTitle = request.POST.get('jobTitle')
        jobType = request.POST.get('jobType')
        jobDescription = request.POST.get('jobDescription')
        jobLocation = request.POST.get('jobLocation')
        jobSalary = request.POST.get('jobSalary')

        try:
            job = {
            'Title' : jobTitle,
            'Type': jobType,
            'Location' : jobLocation
            }
    
            database.child('jobs').push(job)
            # Redirect to success page
            return home(request)
        except:
        # Failed to create job
            return render(request, 'job_creation.html', {'error': 'Failed to create job'})
    else:
        # Render signup page
        return render(request, 'job_creation.html')

# signin and signup options

def postsignin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Authenticate user with Firebase Realtime Database
            db = firebase.database()
            users = db.child('users').get()
            for user in users.each():
                if user.val().get('email') == email and user.val().get('password') == password:
                    # Set session variables
                    request.session['uid'] = user.key()
                    request.session['user_type'] = user.val().get('user_type')

                    # Redirect based on user type
                    if user.val().get('user_type') == 'admin':
                        return redirect('/adminpage/')
                    else:
                        return home(request)

            # User not found or invalid credentials
            return render(request, 'signin.html', {'error': 'Invalid email or password'})
        except:
            # Failed to sign in user
            return render(request, 'signin.html', {'error': 'Failed to sign in user'})
    else:
        # Render signin page
        return render(request, 'signin.html')


def postsignup(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        
        if password1 != password2:
            # Passwords don't match
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        try:
            # Create user in Firebase Realtime Database
            db = firebase.database()
            user_data = {
                'email': email,
                'password': password1,
                'user_type': user_type
            }
            db.child('users').push(user_data)
            
            # Redirect to success page
            return render(request,'signin.html')
        except:
            # Failed to create user
            return render(request, 'signup.html', {'error': 'Failed to create user'})
    else:
        # Render signup page
        return render(request, 'signup.html')

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
storage = firebase.storage()

def home(request):
    context = {'foo': 'bar'}
    return render(request, 'home.html', context)

def redirect_signin(request):
    return render(request,'signin.html')

def redirect_signup(request):
    return render(request, 'signup.html')

def redirect_delete(request):
    return render(request, 'delete.html')

def redirect_profile(request):
    return render(request, 'profilecreate.html')

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
    """Deletes account of currently logged in user"""
    user = auth.current_user['localId']
    auth.delete_user_account(user['idToken'])
    return render(request, 'home.html')

def postProfile(request):
    """Allows user to customize their profile"""

     #Basic Information

    name = request.POST.get('name')
    title = request.POST.get('title')
    experience = request.POST.get('experience')
    academics = request.POST.get('academics')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    url = request.POST.get('url') #URL for profile photo

    dataBasic = {'Name': name, 'Title': title, 'Exeperience': experience, 'Academics': academics, 'Gender': gender, 'Age': age, 'PhotoURL': url}

    database.child('users').child('profiles').child('basicInfo').push(dataBasic)

    # Contact information

    phone = request.POST.get('phone')
    address = request.POST.get('address')
    email = request.POST.get('email')
    website = request.POST.get('website')

    dataContact = {'Phone': phone, 'Address': address, 'Email': email, 'Website': website}

    database.child('users').child('profiles').child('contactInfo').push(dataContact)

    #Education

    gradDate = request.POST.get('gradDate')
    degree = request.POST.get('degree')
    school = request.POST.get('school')

    dataEducation = {'Date': gradDate, 'Degree': degree, 'School': school}

    database.child('users').child('profiles').child('education').push(dataEducation)

    #Experience

    exp1Date = request.POST.get('exp1Date')
    exp2Date = request.POST.get('exp2Date')
    exp3Date = request.POST.get('exp3Date')

    exp1Title = request.POST.get('exp1Title')
    exp2Title = request.POST.get('exp2Title')
    exp3Title = request.POST.get('exp3Title')

    exp1Company = request.POST.get('exp1Company')
    exp2Company = request.POST.get('exp2Company')
    exp3Company = request.POST.get('exp3Company')

    dataExpDates = {'Date1': exp1Date, 'Date2': exp2Date, 'Date3': exp3Date}
    dataExpTitles = {'Title1': exp1Title, 'Title2': exp2Title, 'Title3': exp3Title}
    dataExpCompany = {'Company1': exp1Company, 'Company2': exp2Company, 'Company3': exp3Company}

    database.child('users').child('profiles').child('experience').child('dates').push(dataExpDates)
    database.child('users').child('profiles').child('experience').child('titles').push(dataExpTitles)
    database.child('users').child('profiles').child('experience').child('company').push(dataExpCompany)

    #Profile Photo
    


    return render(request,'profile.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from email.message import EmailMessage
import pyrebase
import smtplib

SIGNIN_PAGE = '/signin/'

SIGNIN_FILE = 'signin.html'
SIGNUP_FILE = 'signup.html'
PROFILE_FILE = 'profile.html'
JOB_CREATION_FILE = 'job_creation.html'

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
    context = {"jobs":jobs.val()}
    return render(request, 'home.html', context)

def redirect_signin(request):
    return render(request, SIGNIN_FILE)

def redirect_signup(request):
    return render(request, SIGNUP_FILE)
    
def logout(request):
    request.session.flush()
    return redirect(home)

def redirect_profile(request):
    return render(request, PROFILE_FILE)

def redirect_job_creation(request):
    # Check if user is signed in and is an employer
    if 'uid' in request.session and request.session['user_type'] == 'employer':
        return render(request, JOB_CREATION_FILE)
    else:
        return redirect(SIGNIN_PAGE)
    
def redirect_admin(request):
    # Check if user is signed in and is an admin
    if 'uid' in request.session and request.session['user_type'] == 'admin':
        names = []
        emails = []
        userids = []
        titles = []
        descriptions = []
        jobids = []
        jobs = database.child('jobs').get()
        users = database.child('users').get()

        # Loop iterates through users in the database and stores their userids, names and emails in 3 lists, unless they are admin
        for user in users.each():
            if (user.val()['user_type'] == 'admin'):
                continue
            else:
                names.append(user.val()['Name'])
                emails.append(user.val()['email'])
                userids.append(user.key())

        # Loop iterates through jobs in the database and stores their jobids, titles and descriptions in 3 lists
        for job in jobs.each():
            titles.append(job.val()['Title'])
            descriptions.append(job.val()['Description'])
            jobids.append(job.key())


        userdata = {'userids': userids, 'names': names, 'emails': emails}
        jobdata = {'jobids': jobids, 'titles': titles, 'descriptions': descriptions}

        userrows = list(zip(*userdata.values()))
        jobrows = list(zip(*jobdata.values()))
        return render(request, 'admin_p.html', {"rows":userrows, "jobrows": jobrows})
    else:
        return redirect(SIGNIN_PAGE)

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
            'Location' : jobLocation,
            'Description' : jobDescription,
            'Salary' : jobSalary,
            'Applicants' : "",
            'Owner' : request.session['uid']
            }
    
            database.child('jobs').push(job)
            # Redirect to success page
            return redirect(home)
        except:
        # Failed to create job
            return render(request, JOB_CREATION_FILE, {'error': 'Failed to create job'})
    else:
        # Render signup page
        return render(request, JOB_CREATION_FILE)
        
def jobview(request):
    jobid = request.GET['id']
    title = database.child("jobs").child(jobid).child("Title").get().val()
    type = database.child("jobs").child(jobid).child("Type").get().val()
    location = database.child("jobs").child(jobid).child("Location").get().val()
    description=database.child("jobs").child(jobid).child("Description").get().val()
    salary=database.child("jobs").child(jobid).child("Salary").get().val()
    context = {
        'Title' : title,
        'Type': type,
        'Location' : location,
        'Description' : description,
        'Salary' : salary,
        'key' : jobid
    }
    return render(request, 'JobDes.html', context)

def applytojob(request):
    if 'uid' in request.session and request.session['user_type'] == 'student':
        jobid = request.GET['id']
        print(jobid)
        userid = request.session['uid']
        print(userid)
        applicantlist = str(database.child("jobs").child(jobid).child("Applicants").get().val())
        if userid not in applicantlist:
            applicantlist+= userid + ","
            newvalue = {'Applicants': applicantlist}
            database.child("jobs").child(jobid).update(newvalue)
        #Add error if already applied
        return redirect(home)
    else:
        return redirect(SIGNIN_PAGE)

def jobmanage(request):
    jobslist = database.child("jobs").shallow().get().val()
    jobsdict={}
    for job in jobslist:
        applicantsdict={}
        if database.child("jobs").child(job).child("Owner").get().val() == request.session['uid']:
            title = database.child("jobs").child(job).child("Title").get().val()
            type = database.child("jobs").child(job).child("Type").get().val()
            location = database.child("jobs").child(job).child("Location").get().val()
            salary=database.child("jobs").child(job).child("Salary").get().val()
            applicants = database.child("jobs").child(job).child("Applicants").get().val()
            list = applicants.split(",")
            while("") in list:
                list.remove("")
            applicantsdict=dict.fromkeys(list)
            for user in list:
                applicantsdict[user]=database.child("users").child(user).get().val()
                del applicantsdict[user]["password"]
            listinginfo = {
                'Title' : title,
                'Type': type,
                'Location' : location,
                'Salary' : salary,
                'jobid' : job,
                'applicants' : applicantsdict
                }
            jobsdict[job]=listinginfo
    context = {
    'data' : jobsdict
        }
    return render(request, 'jobmanage.html', context)
    
def accept(request):
    jobid=request.GET['jobid']
    userid=request.GET['userid']
    email=database.child("users").child(userid).child("email").get().val()
    print("Job Accepted " + jobid + "for " + userid)
    try:
        server = smtplib.SMTP('localhost', 25)
        msg = EmailMessage()
        msg['From'] = 'mailuser@domain'
        msg['To'] = email
        msg['Subject'] = 'Congratulations! You have an upcoming interview'
        body="You've been accepted for an interview for " + database.child("jobs").child(jobid).child("Title").get().val() + " at " + database.child("jobs").child(jobid).child("Company").get().val()
        msg.set_content(body)
        server.send_message(msg)
        server.quit()
        applicantlist = str(database.child("jobs").child(jobid).child("Applicants").get().val())
        if userid in applicantlist:
            newlist=applicantlist.replace(userid + ',', '')
            newvalue = {'Applicants': newlist}
            database.child("jobs").child(jobid).update(newvalue)
    except Exception as e:
        print(e)
    return redirect('/jobmanage')

def decline(request):
    jobid=request.GET['jobid']
    userid=request.GET['userid']
    email=database.child("users").child(userid).child("email").get().val()
    print("Job Declined " + jobid + "for " + userid)
    try:
        server = smtplib.SMTP('localhost', 25)
        msg = EmailMessage()
        msg['From'] = 'mailuser@domain'
        msg['To'] = email
        msg['Subject'] = 'You have been declined'
        body="Your application has been declined for " + database.child("jobs").child(jobid).child("Title").get().val() + " at " + database.child("jobs").child(jobid).child("Company").get().val()
        msg.set_content(body)
        server.send_message(msg)
        server.quit()
        applicantlist = str(database.child("jobs").child(jobid).child("Applicants").get().val())
        if userid in applicantlist:
            newlist=applicantlist.replace(userid + ',', '')
            newvalue = {'Applicants': newlist}
            database.child("jobs").child(jobid).update(newvalue)
    except Exception as e:
        print(e)
    return redirect('/jobmanage')

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
                    request.session['email'] = user.val().get('email')

                    # Redirect based on user type
                    if user.val().get('user_type') == 'admin':
                        return redirect('/adminpage/')
                    else:
                        return redirect(home)

            # User not found or invalid credentials
            return render(request, SIGNIN_FILE, {'error': 'Invalid email or password'})
        except:
            # Failed to sign in user
            return render(request, SIGNIN_FILE, {'error': 'Failed to sign in user'})
    else:
        # Render signin page
        return render(request, SIGNIN_FILE)


def postsignup(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        
        if password1 != password2:
            # Passwords don't match
            return render(request, SIGNUP_FILE, {'error': 'Passwords do not match'})
        
        try:
            # Create user in Firebase Realtime Database
            db = firebase.database()
            user_data = {
                'email': email,
                'password': password1,
                'user_type': user_type,
                'Age': '',
                'Location': 'empty Location',
                'Phone': 'empty Phone',
                'Program': 'empty Program',
                'School' : 'empty School',
                'Email': 'empty Email',
                'Name': 'empty Name',
                'Specialization': 'nothing',
                'Experience': '0',
                'Gender': 'everything',
                'Address': 'Address'


            }
            db.child('users').push(user_data)
            
            # Redirect to success page
            return render(request,SIGNIN_FILE)
        except:
            # Failed to create user
            return render(request, SIGNUP_FILE, {'error': 'Failed to create user'})
    else:
        # Render signup page
        return render(request, 'signup.html')
    
def profileview(request):
    profileid = request.GET['id']
    if 'uid' in request.session:
        if request.session['user_type'] == 'student':
            user_data = database.child("users").child(profileid).get().val()
            completed_fields = sum(bool(user_data.get(key)) for key in user_data)
            total_fields = len(user_data.keys())
            completion = int(completed_fields / total_fields * 100)
            context = {
                'Age': user_data.get("Age"),
                'Location': user_data.get("Location"),
                'Phone': user_data.get("Phone"),
                'Program': user_data.get("Program"),
                'School': user_data.get("School"),
                'Email': user_data.get("Email"),
                'Name': user_data.get("Name"),
                'Specialization': user_data.get("Specialization"),
                'Experience': user_data.get("Experience"),
                'Gender': user_data.get("Gender"),
                'Address': user_data.get("Address"),
                'completion': completion
            }
            return render(request, PROFILE_FILE, context)
        elif request.session['user_type'] == 'employer':
            if database.child("users").child(profileid).child("user_type").get().val() == 'student':
                user_data = database.child("users").child(profileid).get().val()
                completed_fields = sum(bool(user_data.get(key)) for key in user_data)
                total_fields = len(user_data.keys())
                completion = int(completed_fields / total_fields * 100)
                context = {
                    'Age': user_data.get("Age"),
                    'Location': user_data.get("Location"),
                    'Phone': user_data.get("Phone"),
                    'Program': user_data.get("Program"),
                    'School': user_data.get("School"),
                    'Email': user_data.get("Email"),
                    'Name': user_data.get("Name"),
                    'Specialization': user_data.get("Specialization"),
                    'Experience': user_data.get("Experience"),
                    'Gender': user_data.get("Gender"),
                    'Address': user_data.get("Address"),
                    'completion': completion
                    }
                return render(request, PROFILE_FILE, context)
            else:
                #Here we would put the context and all the get functions to take from database
                return render(request, 'Employer_profile.html')
    # If user is not logged in, redirect to login page
    else:
        return redirect('login')


def redirect_edit_profile(request):
    # If user type is student, display student profile
    if 'uid' in request.session and request.session['user_type'] == 'student':
        profileid = request.GET['id']
        Age = database.child("users").child(profileid).child("Age").get().val()
        Location = database.child("users").child(profileid).child("Location").get().val()
        Phone = database.child("users").child(profileid).child("Phone").get().val()
        Program = database.child("users").child(profileid).child("Program").get().val()
        School = database.child("users").child(profileid).child("School").get().val()
        Email = database.child("users").child(profileid).child("email").get().val()
        Name = database.child("users").child(profileid).child("Name").get().val()
        Specialization = database.child("users").child(profileid).child("Specialization").get().val()
        Experience = database.child("users").child(profileid).child("Experience").get().val()
        Gender = database.child("users").child(profileid).child("Gender").get().val()
        Address = database.child("users").child(profileid).child("Address").get().val()

        context = {
            'Age' : Age,
            'Location' : Location,
            'Phone' : Phone,
            'Program' : Program,
            'School' : School,
            'Email' : Email,
            'Name' : Name,
            'Specialization' : Specialization,
            'Experience' : Experience,
            'Gender' : Gender,
            'Address' : Address
        }
    # If user type is employer, display employer profile
    if 'uid' in request.session and request.session['user_type'] == 'employer':
        profileid = request.GET['id']
        Company = database.child("users").child(profileid).child("Company").get().val()
        Vision = database.child("users").child(profileid).child("Vision").get().val()
        Industry = database.child("users").child(profileid).child("Industry").get().val()
        Website = database.child("users").child(profileid).child("Website").get().val()
        Size = database.child("users").child(profileid).child("Size").get().val()
        Location = database.child("users").child(profileid).child("Location").get.val()
        Email = database.child("users").child(profileid).child("email").get().val()
        Name = database.child("users").child(profileid).child("Name").get().val()

        context = {
            'Company' : Company,
            'Vision' : Vision,
            'Industry' : Industry,
            'Website' : Website,
            'Size' : Size,
            'Location' : Location,
            'Email' : Email,
            'Name' : Name
            }

    return render(request, 'profile_edit.html', context)

def edit_profile(request):
    # Retrieve the current user's profile information from the session
    # Edit student profile
    if 'uid' in request.session and request.session['user_type'] == 'student':
        profileid = request.session['uid']
        current_user = firebase.database().child('users').child(profileid).get().val()

        if request.method == 'POST':
            # Get form data
            newAge = request.POST.get('age')
            newlocation = request.POST.get('location')
            newphone = request.POST.get('phone')
            newprogram = request.POST.get('program')
            newschool = request.POST.get('school')
            newemail = request.POST.get('email')
            newname = request.POST.get('name')
            newspecialization = request.POST.get('specialization')
            newexperience = request.POST.get('experience')
            newgender = request.POST.get('gender')
            newaddress = request.POST.get('address')
        
            try:
                # Update the user's information in the database with the form data
                db = firebase.database()
                db.child('users').child(profileid).update({
                    "Age": newAge,
                    "Location": newlocation,
                    "Phone": newphone,
                    "Program": newprogram,
                    "School": newschool,
                    "Email": newemail,
                    "Name": newname,
                    "Specialization": newspecialization,
                    "Experience": newexperience,
                    "Gender": newgender,
                    "Address": newaddress
                })
            
                # Update the corresponding values in the session
                request.session['Age'] = newAge
                request.session['Location'] = newlocation
                request.session['Phone'] = newphone
                request.session['Program'] = newprogram
                request.session['School'] = newschool
                request.session['Email'] = newemail
                request.session['Name'] = newname
                request.session['Specialization'] = newspecialization
                request.session['Experience'] = newexperience
                request.session['Gender'] = newgender
                request.session['Address'] = newaddress
            
                # Redirect to success page
                return redirect(home)
            except:
                # Failed to update profile
                return render(request, 'profile_edit.html', {'error': 'Failed to update profile'})
        else:
            # Set the default values of the form fields to the current user's information
            return render(request, 'profile_edit.html', current_user)
    
    # Edit employer profile
    if 'uid' in request.session and request.session['user_type'] == 'employer':
        profileid = request.session['uid']
        current_user = firebase.database().child('users').child(profileid).get().val()
        if request.method == 'POST':
            # Get form data
            newCompany = request.POST.get('company')
            newlocation = request.POST.get('location')
            newVision = request.POST.get('vision')
            newIndustry = request.POST.get('industry')
            newWebsite = request.POST.get('school')
            newemail = request.POST.get('email')
            newname = request.POST.get('name')

            try:
                # Update the user's information in the database with the form data
                db = firebase.database()
                db.child('users').child(profileid).update({
                    "Company": newCompany,
                    "Location": newlocation,
                    "Vision": newVision,
                    "Industry": newIndustry,
                    "Website": newWebsite,
                    "Email": newemail,
                    "Name": newname,
                })
            
                # Update the corresponding values in the session
                request.session['Company'] = newCompany
                request.session['Location'] = newlocation
                request.session['Vision'] = newVision
                request.session['Industry'] = newIndustry
                request.session['Website'] = newWebsite
                request.session['Email'] = newemail
                request.session['Name'] = newname
            
                # Redirect to success page
                return redirect(home)
            except:
                # Failed to update profile
                return render(request, 'profile_edit.html', {'error': 'Failed to update profile'})
        else:
            # Set the default values of the form fields to the current user's information
            return render(request, 'profile_edit.html', current_user)
            
def delete(request):
    jobid=request.GET['jobid']
    database.child("jobs").child(jobid).remove()
    return redirect('/jobmanage')


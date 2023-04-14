from django.test import TestCase, Client
from django.conf import settings as django_settings
import pyrebase
import random

config = {
    "apiKey": "AIzaSyAim4TyliA_tnns9WFI1y5eQBdlMrQm58Q",
    "authDomain": "djangoproject-620c6.firebaseapp.com",
    "databaseURL": "https://djangoproject-620c6-default-rtdb.firebaseio.com/",
    "projectId": "djangoproject-620c6",
    "storageBucket": "djangoproject-620c6.appspot.com",
    "messagingSenderId": "645132885500",
    "appId": "1:645132885500:web:7ffb3a5d868b6c53816679",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


class FunctionalityTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        db = firebase.database()
        users = db.child('users').get()

        self.valid_user = users[0]

        test_val = random.randint(0, 10000000)

        for user in users.each():
            if (users.val().get('email') == str(test_val) + '@gmail.com'):
                test_val += 1

        self.invalid_user_email = str(test_val) + '@gmail.com'
        self.invalid_user_password = 'password'

        return True

    def test_failed_signin(self):
        temp = 1

        session = self.client.session
        session["uid"] = temp
        session.save()

        session_cookie_name = django_settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie_name] = session.session_key

        self.client.post('/postsignin/',
                         {'email': self.invalid_user_email,
                          'pass': self.invalid_user_password})

        self.assertEqual(self.client.session["uid"], temp)

    def test_signin(self):
        self.client.post('/postsignin/',
                         {'email': self.valid_user.val().get('email'),
                          'password': self.valid_user.val().get('password')})

        self.assertEqual(self.client.session["uid"], self.valid_user.key())

    def test_logout(self):
        self.client.get('/logout/')

        self.assertEqual(len(self.client.session.keys()), 0)

    def test_create_user(self):
        self.client.post('/postsignup/',
                         {'email': self.invalid_user_email,
                          'password1': self.invalid_user_password,
                          'password2': self.invalid_user_password,
                          'user_type': 'student'})

        users = firebase.database().child('users').get()
        failure = True

        for user in users.each():
            if user.val().get('email') == self.invalid_user_email and user.val().get('password') == self.invalid_user_password:
                failure = False
                firebase.database().child('users').child(str(user.key())).remove()
                break

        self.assertEqual(failure, False)

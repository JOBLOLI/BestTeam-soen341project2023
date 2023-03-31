from django.test import TestCase, Client


class ViewsTestCase(TestCase):
    def setUp(self):
        return True

    def test(self):
        self.assertEqual(True, True)

    def test_bad_request(self):
        client = Client()
        response = client.get('bad_request')
        self.assertEqual(response.status_code, 404)

    def test_home(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        client = Client()
        response = client.get('/signin/')
        self.assertEqual(response.status_code, 200)
    
    def test_signup(self):
        client = Client()
        response = client.post('/signup/')
        self.assertEqual(response.status_code, 200)
        # response = client.post('/signup/',
        #                        {'email': 'test@test.com',
        #                         'pass': 'password',
        #                         'name': 'testname'})
        # login = client.get('/signup/', 
        #                    {'email': 'test1@test.com',
        #                     'pass': 'password'},
        #                    follow=True)
        # login = client.login(email='test@test.com', password='password')
        # print(login.content)

    def test_logout(self):
        client = Client()
        response = client.post('/create_job/')
        self.assertEqual(response.status_code, 200)

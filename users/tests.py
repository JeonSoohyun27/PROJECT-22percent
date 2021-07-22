import json
import unittest
import jwt

from django.test import TestCase, Client

from users.models   import User, Bank
from my_settings    import SECRET_KEY, ALGORITHM

class EmailSignupTest(TestCase):
    def setUp(self):
        Bank.objects.create(
            id   = 1,
            name = "농협은행"
        )

        User.objects.create(
            id              = 1,
            name            = 'Brendan Eich',
            email           = 'BrendanEich@gmail.com',
            password        = '$2b$12$Yb42qFbxBA7zHMPIN9hVz.6BJA0HtT0bOgILp/fy/J5czCPT505Gy',
            deposit_bank_id = 1,
            deposit_account = "12345678901234567",
        )

    def tearDown(self):
        User.objects.all().delete()
        Bank.objects.all().delete()

    def test_email_signup_post_success(self):
        client = Client()
        user = {
            'email'    : 'GuidovanRossum@gmail.com',
            'password' : 'P@ssW0rd'
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        user         = User.objects.get(email=user['email'])
        access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'accessToken': access_token})
    
    def test_email_signup_post_duplicate_email(self):
        client = Client()
        user = {
            'email': 'BrendanEich@gmail.com',
            'passwrod': "P@ssW0rd"
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "DUPLICATE_EMAIL"})

    def test_email_signup_post_invalid_email(self):
        client = Client()
        user = {
            'email': '111@gmail.111',
            'password': "P@ssW0rd"
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_EMAIL"})

    def test_email_signup_post_invalid_password(self):
        client = Client()
        user = {
            'email': 'GuidovanRossum@gmail.com',
            'password': "1234567"
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_PASSWORD"})

    def test_email_signup_post_key_error(self):
        client = Client()
        user = {
            'not_a_key_email': 'GuidovanRossum@gmail.com',
            'password': "P@ssW0rd"
        }

        response = client.post('/users/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

class EmailSigninTest(TestCase):
    def setUp(self):
        Bank.objects.create(
            id = 1,
            name = "농협은행"
        )

        User.objects.create(
            id              = 1,
            name            = 'Brendan Eich',
            email           = 'BrendanEich@gmail.com',
            password        = '$2b$12$2z0eQ/bEGgso2xAT1Q6CJupZfAOK1gXgMO1KAJ0/OuMT0gdR6ZJae',
            deposit_bank_id = 1,
            deposit_account = "12345678901234567",

        )

    def tearDown(self):
        User.objects.all().delete()
        Bank.objects.all().delete()

    def test_email_signin_post_success(self):
        client = Client()
        user = {
            'email'    : 'BrendanEich@gmail.com',
            'password' : 'P@ssW0rd'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        user         = User.objects.get(email=user['email'])
        access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"accessToken": access_token})

    def test_email_signup_post_invalid_user(self):
        client = Client()
        user = {
            'email'    : 'BrendanEich@gmail.com',
            'password' : 'Wrong_P@ssW0rd'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})

    def test_email_signup_post_not_exist_user(self):
        client = Client()
        user = {
            'email'    : 'NoExist@gmail.com',
            'password' : 'P@ssW0rd'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})

    def test_email_signup_post_key_error(self):
        client = Client()
        user = {
            'not_a_key_email' : 'NoExist@gmail.com',
            'password'        : 'P@ssW0rd'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

if __name__ == "__main__":
    unittest.main()

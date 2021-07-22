import json
import unittest
from unittest.mock  import patch, MagicMock

from django.test import TestCase, Client

from users.models   import User, Bank

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

        access_token = response.json()['accessToken']

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

        access_token = response.json()['accessToken']

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

@patch('users.views.requests')
class KakaoSigninTest(TestCase):
    def setUp(self):
        Bank.objects.create(
            id   = 1,
            name = "농협은행"
        )

        User.objects.create(
            id              = 1,
            kakao_id        = 1234567890,
            deposit_bank_id = 1,
            deposit_account = "12345678901234"
        )

    def tearDown(self):
        User.objects.all().delete()
        Bank.objects.all().delete()

    @patch('users.views.requests')
    def test_kakao_signin_get_signup_success(self, request, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                    'id': 12341234,
                    'connected_at': '2021-07-19T14:29:58Z', 
                    'properties': {
                        'nickname': '테스트'
                    }, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile': {
                            'nickname': '테스트'
                        }
                    }
                }
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        client   = Client()
        headers  = {'HTTP_AUTHORIZATION': 'fake access_token'}
        response = client.post("/users/signin/kakao", **headers)

        access_token = response.json()['accessToken']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"accessToken": access_token})

    @patch('users.views.requests')
    def test_kakao_signin_get_signin_success(self, request, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                    'id': 1234567890,
                    'connected_at': '2021-07-19T14:29:58Z', 
                    'properties': {
                        'nickname': '테스트'
                    }, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile': {
                            'nickname': '테스트'
                        }
                    }
                }
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        client   = Client()
        headers  = {'HTTP_AUTHORIZATION': 'fake access_token'}
        response = client.post("/users/signin/kakao", **headers)

        access_token = response.json()['accessToken']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"accessToken": access_token})

    @patch('users.views.requests')
    def test_kakao_signin_get_key_error(self, request, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                    'not_a_key_id': 1234567890,
                    'connected_at': '2021-07-19T14:29:58Z', 
                    'properties': {
                        'nickname': '테스트'
                    }, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile': {
                            'nickname': '테스트'
                        }
                    }
                }
        mocked_requests.post = MagicMock(return_value = MockedResponse())
        
        client   = Client()
        headers  = {'HTTP_AUTHORIZATION': 'fake access_token'}
        response = client.post("/users/signin/kakao", **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        
    def test_kakao_signin_get_no_token(self, request):
        client   = Client()
        response = client.post("/users/signin/kakao")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "NEED_LOGIN"})
        
if __name__ == '__main__':
    unittest.main()

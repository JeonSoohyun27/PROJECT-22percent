import json

import bcrypt, jwt
import requests

from django.http      import JsonResponse
from django.views     import View

from users.models   import User
from users.utils    import create_random_account
from my_settings    import SECRET_KEY, ALGORITHM

KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

class EmailSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.validate_regex(data):
                return JsonResponse({"message": "VALIDATION_ERROR"}, status=400) 

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(
                email           = data['email'],
                password        = hashed_password.decode(),
                deposit_bank_id = 1,
                deposit_account = create_random_account()
            )

            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"accessToken": access_token}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class EmailSigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({"accessToken": access_token}, status=200)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class KakaoSigninView(View):
    def post(self, request):
        try:
            kakao_access_token = request.headers.get('Authorization', None)

            if not kakao_access_token:
                return JsonResponse({"message": "NEED_LOGIN"}, status=401)

            headers  = {"Authorization": f"Bearer {kakao_access_token}"}
            response = requests.post(KAKAO_USER_INFO_URL, headers=headers)

            kakao_profile = response.json() 
            kakao_id      = kakao_profile['id']

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    'deposit_bank_id' : 1,
                    'deposit_account' : create_random_account()
                }
            )

            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({"accessToken": access_token}, status=(201 if is_created else 200))
    
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

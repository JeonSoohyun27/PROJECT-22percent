import json, re
import bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View

from users.models   import User
from users.utils    import create_random_account
from my_settings    import SECRET_KEY, ALGORITHM

EMAIL_REGEX    = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

class EmailSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not re.match(EMAIL_REGEX, data['email']):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

            if not re.match(PASSWORD_REGEX, data['password']):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

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

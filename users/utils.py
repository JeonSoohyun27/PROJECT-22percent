import uuid
import jwt

from django.http      import JsonResponse
from django.db.models import Q

from users.models   import User
from my_settings    import SECRET_KEY, ALGORITHM

def user_validator(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            acces_token = request.headers.get('Authorization', None)

            if not acces_token:
                return JsonResponse({"message": "NEED_LOGIN"}, status=401)

            payload      = jwt.decode(acces_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload["user_id"])
            request.user = user

            return function(self, request, *args, **kwargs)
        
        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "EXPIRED_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

    return wrapper

def create_random_account():
    random_account = str(uuid.uuid4().int>>64)[0:17]
    
    if User.objects.filter(Q(deposit_account=random_account) | Q(withdrawal_account=random_account)).exists():
        return create_random_account()

    return random_account

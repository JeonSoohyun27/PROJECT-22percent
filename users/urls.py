from django.urls    import path

from users.views    import EmailSignupView, EmailSigninView, KakaoSigninView

urlpatterns = [
    path('/signup'       , EmailSignupView.as_view()),
    path('/signin'       , EmailSigninView.as_view()),
    path('/signin/kakao' , KakaoSigninView.as_view()),
]

from django.urls    import path

from users.views    import EmailSignupView

urlpatterns = [
    path('/signup', EmailSignupView.as_view()),
]

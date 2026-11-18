from django.urls import path
from .views import HomeView, UserSignUpView, EmailVerifyView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup", UserSignUpView.as_view(), name="google signup"),
    path("email", EmailVerifyView.as_view(), name="email verification")
]
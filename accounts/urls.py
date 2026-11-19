from django.urls import path
from .views import HomeView, UserSignUpView, EmailVerifyView, SigninView, PasswordResetView, ResetVerifyView, PasswordChangeView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup", UserSignUpView.as_view(), name="email signup"),
    path("email", EmailVerifyView.as_view(), name="email verification"),
    path("signin", SigninView.as_view(), name="email signin"),
    path("token/refresh", TokenRefreshView.as_view(), name="token refresh"),
    path("password/reset", PasswordResetView.as_view()),
    path("password/change", PasswordChangeView.as_view()),
    path("password/reset/verify", ResetVerifyView.as_view()),
    path("logout", LogoutView.as_view()),
]
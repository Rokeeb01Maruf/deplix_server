from django.urls import path
from .views import HomeView, UserSignUpView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup", UserSignUpView.as_view(), name="google signup"),
]
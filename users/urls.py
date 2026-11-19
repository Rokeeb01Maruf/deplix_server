from django.urls import path
from .views import GetMeView

urlpatterns = [
    path("me", GetMeView.as_view())
]
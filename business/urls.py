from django.urls import path
from .views import BusinessView

urlpatterns = [
    path("business", BusinessView.as_view())
]
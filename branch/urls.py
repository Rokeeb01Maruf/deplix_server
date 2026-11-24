from django.urls import path
from .views import BranchView

urlpatterns = [
    path("branch", BranchView.as_view())
]
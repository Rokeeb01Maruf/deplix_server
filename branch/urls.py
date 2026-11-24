from django.urls import path
from .views import BranchView, SingleBranchSerializer

urlpatterns = [
    path("branch", BranchView.as_view()),
    path("branch/<string :branch_id>", SingleBranchSerializer.as_view())
]
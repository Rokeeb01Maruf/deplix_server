from django.urls import path
from .views import SupplierView

urlpatterns = [
    path("suppliers", SupplierView.as_view())
]
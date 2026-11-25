from django.urls import path
from .views import SupplierView

urlpatterns = [
    path("supplier", SupplierView.as_view())
]
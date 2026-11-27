from django.urls import path
from .views import SupplierView, SingleSupplierView

urlpatterns = [
    path("suppliers", SupplierView.as_view()),
    path("suppliers/<uuid:supplier_id>", SingleSupplierView.as_view())
]
from rest_framework.permissions import BasePermission
from branch.permissions import IsEmployee

class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        employee_exist = request.user.employee_records.filter(is_active=True).exists()
        return bool(request.user.is_authenticated and employee_exist)

class IsRightEmployee(IsEmployee):
    def has_permission(self, request, view):
        employee = request.user.employee_records(is_active=True).exists()
        query = view.kwargs.get("supplier_id")

        uuid = self.is_valid_uuid(query)

        return bool(request.user.is_authenticated and employee and uuid)
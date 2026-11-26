from rest_framework.permissions import BasePermission

class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        employee_exist = request.user.employee_records.filter(is_active=True).exists()
        return bool(request.user.is_authenticated and employee_exist)
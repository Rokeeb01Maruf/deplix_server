from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        business = request.user.business
        role = user.employee_records.filter(is_active=True, role="owner", business=business).exists()
        return bool(request.user.is_authenticated and role)
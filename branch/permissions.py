from rest_framework.permissions import BasePermission
import uuid
from branch.models import Branch

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        business = request.user.business
        role = user.employee_records.filter(is_active=True, role="owner", business=business).exists()
        return bool(request.user.is_authenticated and role)

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        business = request.user.business
        role = user.employee_records.filter(is_active=True, role="staff", business=business).exists()
        return bool(request.user.is_authenticated and role)

class IsBM(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        business = request.user.business
        role = user.employee_records.filter(is_active=True, role="bm", business=business).exists()
        return bool(request.user.is_authenticated and role)

class IsEmployee(BasePermission):
    @staticmethod
    def is_valid_uuid(value):
        try:
            uuid.UUID(value)
            return True
        except (ValueError, AttributeError, TypeError):
            return False
        
    def has_permission(self, request, view):
        branch_id = view.kwargs.get("branch_id")
        user = request.user
        employee = user.employee_records.filter(is_active=True).first()

        if not employee:
            return False

        roles = ["staff", "bm"]

        if employee.role in roles and branch_id != "my_branch":
            return False

        if employee.role == "owner" and self.is_valid_uuid(branch_id) != True:
            return False
        else:
            branch = Branch.objects.filter(id=branch_id, business=employee.business).first()
            if not branch:
                return False
            request.branch = branch
            return True
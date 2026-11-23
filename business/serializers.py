from rest_framework import serializers
from branch.models import Branch
from .models import Business
from django.db import transaction
from branch.serializers import BranchSerializer
from employee.models import Employee

class BusinessSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    class Meta:
        model = Business
        fields = "__all__"
        read_only_fields = ["id", "is_active", "branches", "owner"]
        extra_kwargs = {
            "id" : { "read_only" : True },
            "owner" : { "read_only" : True },
        }

    def create(self, validated_data):
        owner = self.context.get("user")
        with transaction.atomic():
            business = Business.objects.create(owner=owner, **validated_data)

            branch = Branch.objects.create(
                name="Main Branch",
                is_primary=True,
                business=business
            )

            employee = Employee.objects.create(
                user=owner,
                role="owner",
                business=business,
                branch=branch
            )

            return business
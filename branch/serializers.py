from .models import Branch
from rest_framework import serializers
from employee.serializers import Employeeserializer

class BranchSerializer(serializers.ModelSerializer):
    employee_records = Employeeserializer(many=True, read_only=True)
    class Meta:
        model = Branch
        fields = "__all__"
        extra_kwargs={
            "business" : {"read_only" : True}
        }

    def create(self, validated_data):
        branch = Branch.objects.create(**validated_data, business=self.context.get("business"))

        return branch
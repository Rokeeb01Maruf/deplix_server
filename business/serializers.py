from rest_framework import serializers
from branch.models import Branch
from .models import Business
from django.db import transaction

class CreateBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"
        extra_kwargs = {
            "id" : { "read_only" : True },
            "owner" : { "read_only" : True }
        }

    def create(self, validated_data):
        owner = self.context.get("user")
        with transaction.atomic():
            business = Business.objects.create(owner=owner, **validated_data)

            branch = Branch.objects.create(
                name=f"{business.name}-HQ",
                is_primary=True,
                business=business
            )

            return business
from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ["id", "is_active"]
        extra_kwargs = {
            "id" : { "read_only" : True },
            "is_active" : {"read_only" : True}
        }

    def create(self, validated_data):
        business = self.context.get("business")
        return Supplier.objects.create(**validated_data, business=business)
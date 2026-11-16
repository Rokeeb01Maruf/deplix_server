from rest_framework import serializers
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password" : { "write_only" : True },
            "email" : { "validators" : [] },
            "first_name" : { "required" : True },
            "last_name" : { "required" : True }
        }

    def validate_password(self, value):
        if len(value) < 8 :
            raise serializers.ValidationError("password is too short")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
from rest_framework import serializers
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "id"]
        extra_kwargs = {
            "id" : {"read_only" : True},
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

class EmailVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    id = serializers.UUIDField()

    def create(self, validated_data):
        user_id = validated_data.get("id")
        user = User.objects.filter(id=user_id).first()

        if user.is_email_verified:
            raise ValueError("email already verified")

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return user

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        return User.objects.get(email=validated_data.get("email"))

class PasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return User.objects.get(email=validated_data.get("email"))

class ResetVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, min_length=6)
    email = serializers.EmailField()

    def create(self):
        return User.objects.get('email')

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data.get("email"))

        user.set_password(validated_data.get("password"))
        user.save(update_fields=["password"])

        return user
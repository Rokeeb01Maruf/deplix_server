import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager

class Business(models.Model):
    pass


class User(AbstractUser):
    USER_CHOICES = (("admin", "admin"), ("user", "user"))
    PROVIDER_CHOICES = (("google", "google"), ("email", "email"), ("both", "both"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(choices=USER_CHOICES, max_length=5, default=USER_CHOICES[1][0])
    auth_provider = models.CharField(choices=PROVIDER_CHOICES, max_length=6, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None

    REQUIRED_FIELDS = []

    USERNAME_FIELD="email"

    objects = UserManager()

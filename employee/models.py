import uuid
from django.db import models
from accounts.models import User
from business.models import Business

class Employee(models.Model):

    ROLE_CHOICES = (("owner", "owner"), ("bm", "bm"), ("staff", "staff"))

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='employee_records'
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=6)
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name='employees'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(blank=True, null=True)
from django.db import models
import uuid
from accounts.models import User

class Business(models.Model):
    class Meta:
        db_table = 'business'

    BUSINESS_TYPES = (("retail", "retail"), ("wholesale", "wholesale"), ("mixed", "mixed"), ("distribution" ,"distribution"),("other", "other"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    type = models.CharField(choices=BUSINESS_TYPES, max_length=12)
    logo = models.URLField(blank=True, max_length=500)
    phone = models.CharField(max_length=20, blank=True)
    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='business'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
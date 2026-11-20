from django.db import models
from django.db.models.functions import Lower
import uuid
from business.models import Business

class Branch(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    business = models.ForeignKey(
        Business,
        on_delete=models.PROTECT,
        related_name='branches'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='branch'
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                fields=["business", "name"],
                name="unique_branch_per_business"
            )
        ]

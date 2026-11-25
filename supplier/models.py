from django.db import models
from django.db.models.functions import Lower
import uuid
from business.models import Business

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField( blank=True)
    address = models.CharField(max_length=255, blank=True)
    business = models.ForeignKey(
        Business,
        related_name='suppliers',
        on_delete=models.PROTECT
    )
    note = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "suppliers"
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "business",
                name = "uniques_supplier_per_business"
            )
        ]
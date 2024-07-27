# webapp/utils/models.py
import uuid
from django.db import models


class CommonFields(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True, editable=False)
    updated_by = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        abstract = True  # Making this model abstract to avoid database table creation

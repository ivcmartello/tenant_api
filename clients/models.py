"""Clients models."""
import os
import uuid

from django.db import models
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase


class Client(TenantBase):
    """Client model."""

    REQUIRED_FIELDS = ("document", "name", "paid_until", "schema_name", "on_trial")
    document = models.CharField(max_length=18, null=False, blank=False)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    domain_url = models.URLField(blank=True, null=True, default=os.getenv("DOMAIN"))
    on_trial = models.BooleanField(default=True)
    paid_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Domain(DomainMixin):
    pass

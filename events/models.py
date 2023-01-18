import uuid

from django.db import models

from clients.models import Client


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=300)
    
    created_by = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

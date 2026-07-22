import uuid

from django.db import models


class UUIDTimestampedModel(models.Model):
    """Base abstrata para entidades com UUID e timestamps de auditoria básica."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedAndUpdatedAt(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

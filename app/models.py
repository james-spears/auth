from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import unique_slugify


class Model(models.Model):
    class Meta:
        abstract = True
        ordering = ['updated_at']

    # Automatically sets the creation date
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically updates the field on each save
    updated_at = models.DateTimeField(auto_now=True)

    # Deleting just sets the deleted flag to True
    deleted = models.BooleanField(default=False)


class SlugModel(Model):
    class Meta:
        abstract = True
        ordering = ['updated_at']

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=False, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or unique_slugify(
            self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UUIDModel(Model):
    class Meta:
        abstract = True
        ordering = ['updated_at']

    uuid = models.UUIDField(_("UUID"), default=uuid4,
                            primary_key=False, editable=False, db_index=True)

    def __str__(self):
        return str(self.uuid)

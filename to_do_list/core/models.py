from django.db import models
from django.contrib.contenttypes.models import ContentType


class ParaTag(models.Model):
    """Model representing tags used to categorize various entities."""

    title = models.CharField(max_length=30, unique=True, verbose_name="Tag")

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('title',)

    def __str__(self):
        return self.title

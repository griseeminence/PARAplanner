from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Тег")

    def __str__(self):
        return self.title


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('tag', 'content_type', 'object_id')




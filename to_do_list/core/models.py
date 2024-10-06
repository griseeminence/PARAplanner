from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Забыл сменить название, созданы миграции с двумя разными моделями Tag
# переименовал в ParaTag - попробовать обновить. Если что - снести базу




class ParaTag(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Тег")

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('title',)

    def __str__(self):
        return self.title





# class ParaTag(models.Model):
#     title = models.CharField(max_length=30, unique=True, verbose_name="Тег")
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
#                                      verbose_name='Тип Контента')
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
#         ordering = ('title',)
#
#     def __str__(self):
#         return self.title


# class ParaTaggedItem(models.Model):
#     tag = models.ForeignKey(ParaTag, on_delete=models.CASCADE, verbose_name="Тег")
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True,
#                                      verbose_name='Тип Контента')
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
#         ordering = ('-created',)
#         unique_together = ('tag', 'content_type', 'object_id')

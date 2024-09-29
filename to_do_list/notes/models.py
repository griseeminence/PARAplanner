from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from comments.models import Comment
from para.models import Area, Project, Resource

User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_archived = models.BooleanField(default=False, verbose_name='Архив')
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ('created',)

    def __str__(self):
        return self.title

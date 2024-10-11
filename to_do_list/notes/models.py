from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image
from comments.models import Comment
from core.models import ParaTag
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
    tags = models.ManyToManyField(ParaTag, related_name='notes', blank=True, verbose_name='Тег')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обложка')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.cover_image:
            img = Image.open(self.cover_image.file)  # Используем .file для доступа к объекту файла
            img = img.resize((300, 365))  # Укажите желаемый размер
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)  # Можно указать другой формат и качество
            thumb_file = ContentFile(thumb_io.getvalue(), name=self.cover_image.name)
            self.cover_image.save(self.cover_image.name, thumb_file, save=False)

        super().save(*args, **kwargs)

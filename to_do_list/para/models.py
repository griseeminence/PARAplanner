from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from PIL import Image
from comments.models import Comment
from core.models import ParaTag

User = get_user_model()

# TODO: Добавить модель архива. Придумать, как взаимодействовать
# т.е. как пихать все возможные модели в один архив
# upd: Пока используем флаги is_archived в каждой модели. При необходимости, создам
# GenericForeignKey для модели Archive (сейчас обойдусь без новой модели).


STATUS_CHOICES = [
    ('active', 'Активный'),
    ('completed', 'Завершенный'),
    ('on_hold', 'Отложенный'),
]

PRIORITY_CHOICES = [
    (1, 'Низкий'),
    (2, 'Средний'),
    (3, 'Высокий'),
]


class BaseParaModel(models.Model):
    title = models.CharField(max_length=25, verbose_name='Заголовок')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    is_archived = models.BooleanField(default=False, verbose_name='Архив')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    deadline = models.DateField(null=True, blank=True, verbose_name="Дедлайн")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="Приоритет")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обложка')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.cover_image:
            img = Image.open(self.cover_image.file)  # Используем .file для доступа к объекту файла
            img = img.resize((300, 365))  # Укажите желаемый размер
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)  # Можно указать другой формат и качество
            thumb_file = ContentFile(thumb_io.getvalue(), name=self.cover_image.name)
            self.cover_image.save(self.cover_image.name, thumb_file, save=False)

        super().save(*args, **kwargs)


class Area(BaseParaModel):
    tags = models.ManyToManyField(ParaTag, related_name='areas', blank=True, verbose_name='Тег')

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'
        ordering = ('title',)

    def __str__(self):
        return (
            f'Область: {self.title}'
            f'Пользователя: {self.author}'
        )


class Project(BaseParaModel):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='projects', blank=True, null=True)
    tags = models.ManyToManyField(ParaTag, related_name='projects', blank=True, verbose_name='Тег')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ('title',)

    def __str__(self):
        return (
            f'Проект: {self.title}'
            f'Пользователя: {self.author}'
            f'Принадлежит области: {self.area}'
        )


class Resource(BaseParaModel):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='resources', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='resources', null=True, blank=True)
    tags = models.ManyToManyField(ParaTag, related_name='resources', blank=True, verbose_name='Тег')
    resource_type = models.ForeignKey('ResourceType', on_delete=models.SET_NULL, verbose_name='Тип ресурса', null=True,
                                      blank=True)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ('title',)

    def __str__(self):
        return (
            f'Ресурс: {self.title}'
            f'Пользователя: {self.author}'
        )


class ResourceType(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Тип ресурса')

    def __str__(self):
        return self.title

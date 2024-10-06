from django.contrib.auth import get_user_model
from django.db import models
from para.models import BaseParaModel, Area, Resource, Project

User = get_user_model()

STATUS_CHOICES = [
    (0, 'Ожидает'),
    (1, 'В процессе'),
    (2, 'Выполнено'),
    (3, 'Отложено'),
    (4, 'Архив'),
]


# class Tag(models.Model):
#     title = models.CharField('Название тега', max_length=25, unique=True)
#     description = models.TextField('Описание и примеры использования', max_length=100)
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name = 'ТегУДАЛИТЬМОДЕЛЬ'
#         verbose_name_plural = 'ТегиУДАЛИТЬМОДЕЛЬ'
#
#     def __str__(self):
#         return self.title


class Task(BaseParaModel):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        author = self.author.username if self.author else "Unknown Author"
        area = self.area if self.author else "Without Area"
        project = self.project if self.author else "Without Project"
        resource = self.resource if self.author else "Without Resource"
        return (
            f'Задача: {self.title}'
            f'Пользователя: {author}'
            f'Принадлежит области: {area}'
            f'Принадлежит проекту: {project}'
            f'Принадлежит ресурсу: {resource}'
        )

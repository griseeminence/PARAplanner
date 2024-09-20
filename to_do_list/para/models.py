from django.contrib.auth import get_user_model
from django.db import models

from tasks.models import Task

User = get_user_model()


#TODO: Добавить модель архива. Придумать, как взаимодействовать
# т.е. как пихать все возможные модели в один архив


class Area:
    title = models.CharField('Область', max_length=25)
    description = models.TextField('Описание', max_length=1000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'
        ordering = ('title',)

    def __str__(self):
        return (
            f'Область: {self.title}'
            f'Пользователя: {self.author}'
        )


class Project:
    title = models.CharField('Область', max_length=25)
    description = models.TextField('Описание', max_length=1000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='projects')

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


class Resource:
    title = models.CharField('Область', max_length=25)
    description = models.TextField('Описание', max_length=1000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурс'
        ordering = ('title',)

    def __str__(self):
        return (
            f'Ресурс: {self.title}'
            f'Пользователя: {self.author}'
        )

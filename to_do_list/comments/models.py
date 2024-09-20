from django.contrib.auth import get_user_model
from django.db import models

from tasks.models import Task

User = get_user_model()

#TODO: использовать обобщённые связи (Generic Relations)
# изменить привязку к tasks, сделав комментарии общедоступными для любой модели. Пример ниже
# Обобщённые поля для связи с любой моделью
# content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
# object_id = models.PositiveIntegerField()
# content_object = GenericForeignKey('content_type', 'object_id')



class Comment(models.Model):
    text = models.TextField('Текст комментария', max_length=2000)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Отредактировано')
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return (
            f"Комментарий пользователя {self.author}"
            f"Дата публикации комментария: {self.created}"
            f"Комментарий к задаче: {self.task}"
        )
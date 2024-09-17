from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

STATUS_CHOICES = [
        (0, 'Ожидает'),
        (1, 'В процессе'),
        (2, 'Выполнено'),
        (3, 'Отложено'),
        (4, 'Архив'),
    ]

class Task(models.Model):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True, max_length=1000)
    status = models.IntegerField('Статус', choices=STATUS_CHOICES, default=0)
    due_date = models.DateField('Дата выполнения', blank=True, null=True)
    priority = models.BooleanField('Приоритет', default=False)
    # attachment = models.FileField('Файл', blank=True, null=True)
    author = models.ForeignKey(User, verbose_name='Автор записи', blank=True, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown Author"
        return f'{self.title} by {author_name}. Status: {self.status}'

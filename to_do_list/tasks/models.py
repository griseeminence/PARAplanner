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



class Tag(models.Model):
    title = models.CharField('Название тега', max_length=25, unique=True)
    description = models.TextField('Описание и примеры использования', max_length=100)
    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True, max_length=1000)
    status = models.IntegerField('Статус', choices=STATUS_CHOICES, default=0)
    due_date = models.DateField('Дата выполнения', blank=True, null=True)
    priority = models.BooleanField('Приоритет', default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', blank=True, null=True)
    author = models.ForeignKey(User, verbose_name='Автор записи', blank=True, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tag_tasks')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown Author"
        return f'{self.title} by {author_name}. Status: {self.status}'



from django.contrib.auth.models import AbstractUser
from django.db import models

#TODO: Добавить валидатор для уникальности email

class User(AbstractUser):
    """Модель пользователей."""
    email = models.EmailField(
        'Email',
        max_length=200,
        unique=True, )
    first_name = models.CharField(
        'Имя',
        max_length=150)
    last_name = models.CharField(
        'Фамилия',
        max_length=150)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

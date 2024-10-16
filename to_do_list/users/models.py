from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model extending the built-in AbstractUser."""

    email = models.EmailField(
        'Email',
        max_length=200,
        unique=True,
    )
    first_name = models.CharField(
        'First Name',
        max_length=150
    )
    last_name = models.CharField(
        'Last Name',
        max_length=150
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id',)

    def __str__(self):
        return self.username

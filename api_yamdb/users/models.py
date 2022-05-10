from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    )
    role = models.CharField('Роль', choices=CHOICES, default='user',
                            max_length=15)
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return self.username

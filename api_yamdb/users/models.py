from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


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
    email = models.EmailField(max_length=254, blank=False, unique=True)
    confirmation_code = models.TextField('Код подтверждения', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.CheckConstraint(check=~Q(username='me'),
                                   name='username_not_me')
        ]

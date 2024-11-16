from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(
        'E-mail', max_length=254,
        unique=True,
        help_text='Введите email пользователя',
    )
    username = models.CharField(
        'Логин', max_length=150, unique=True,
        validators=[username_validator],
        help_text='Введите логин поьзователя',
    )
    first_name = models.CharField(
        'Имя', max_length=150,
        help_text='Введите имя пользователя',
    )
    last_name = models.CharField(
        'Фамилия', max_length=150,
        help_text='Введите фамилию пользователя',
    )

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    class Meta:
        ordering = ('email', 'id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'

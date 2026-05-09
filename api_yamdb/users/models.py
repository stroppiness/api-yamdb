from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль', max_length=15,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(max_length=6, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

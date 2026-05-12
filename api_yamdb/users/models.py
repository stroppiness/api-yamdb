from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import CONFIRMATION_MAX_LENGTH


class CustomUser(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль', max_length=max(len(value) for value, _ in ROLES),
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(max_length=CONFIRMATION_MAX_LENGTH, blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

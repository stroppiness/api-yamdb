from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    MAX_ROLE_LENGTH = max(len(value) for value, _ in ROLES)

    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль', max_length=MAX_ROLE_LENGTH,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(max_length=6, blank=True)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

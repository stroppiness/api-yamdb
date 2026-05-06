from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLES, default='user')

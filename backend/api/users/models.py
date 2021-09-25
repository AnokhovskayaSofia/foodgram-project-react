from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    # email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        default=UserRole.USER,
        choices=UserRole.choices,
        verbose_name='Роль'
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Информация'
    )

    # email_confirmed = models.BooleanField(
    #     default=False,
    #     verbose_name='Email подтвержден'
    # )

    @property
    def is_admin(self):
        return UserRole.ADMIN == self.role

    @property
    def is_moderator(self):
        return UserRole.MODERATOR == self.role

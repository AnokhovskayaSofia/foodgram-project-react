from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
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

    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден'
    )

    @property
    def is_admin(self):
        return UserRole.ADMIN == self.role


class SubscribedUser(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь')
    user_subscribed_to = models.ForeignKey(
        User,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
        related_name='user_subscribed_to',
        verbose_name='Пользователь на которого подписались')

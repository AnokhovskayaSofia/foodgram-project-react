from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')
    email = models.EmailField(unique=True,
                              verbose_name='Почта')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class SubscribedUser(models.Model):
    user = models.ForeignKey(
        User,
        default=None,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь')
    user_subscribed_to = models.ForeignKey(
        User,
        default=None,
        on_delete=models.CASCADE,
        related_name='user_subscribed_to',
        verbose_name='Пользователь на которого подписались')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'user_subscribed_to'],
                name='unique user per subscribed user'
            ), ]
        verbose_name = 'Подписки пользователя'
        verbose_name_plural = verbose_name

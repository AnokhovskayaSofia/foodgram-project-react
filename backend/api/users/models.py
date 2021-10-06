from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    username = models.CharField(max_length=150,
                                verbose_name='Логин')
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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Item(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой код ингредиента')
    slug = models.SlugField(
        verbose_name='Ингредиент продукта')

    class Meta:
        verbose_name = 'Ингредиент продукта'
        verbose_name_plural = 'Ингредиенты продукта'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='user_api/',
        verbose_name='Изображение')
    text = models.TextField(
        max_length=2000,
        verbose_name='Описание')
    item = models.ManyToManyField(
        Item,
        related_name='recipes',
        verbose_name='Состав')
    price = models.IntegerField(
        default=0,
        verbose_name='Цена')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукт'
        ordering = ['-id']

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    class Meta:
        ordering = ['name']
        fields = ('name', 'measurement_unit')
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой код тега')
    slug = models.SlugField(
        verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=30,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='user_api/',
        verbose_name='Изображение')
    text = models.TextField(
        max_length=1000,
        verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги')
    cooking_time = models.IntegerField(
        # validators=[MaxValueValidator(240, message="invalid value max limit"),
        #             MinValueValidator(1, message="invalid value min limit")],
        default=1,
        verbose_name='Время приготовленмя')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент в рецепте',
        related_name='ingredientrecipe')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_content')
    amount = models.IntegerField(
        default=1,
        verbose_name='Количество ингредиентор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient per recipe'
            ), ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favourite')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favourite')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_in_favorite_per_user'
            ), ]
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


class Shopping(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shoppings')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe_in_shopping_per_user'
            ), ]
        verbose_name = 'В листе покупок'
        verbose_name_plural = verbose_name

class TestModel(models.Model):
    user = models.IntegerField(
        default=1,
        verbose_name='Количество ингредиентор')

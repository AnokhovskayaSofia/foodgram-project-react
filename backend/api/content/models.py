from django.db import models
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название инградиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    class Meta:
        ordering = ['name']
        verbose_name = 'Инградиент'
        verbose_name_plural = 'Инградиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга')
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой код тэга')
    slug = models.SlugField(
        verbose_name='Тэг')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        max_length=30,
        blank=False,
        verbose_name='Название')
    image = models.ImageField(
        upload_to='user_api/',
        blank=False,
        verbose_name='Изображение')
    text = models.TextField(
        max_length=250,
        blank=False,
        verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='IngredientsRecipe',
        related_name='ingredients',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='tags',
        verbose_name='Теги')
    cooking_time = models.IntegerField(
        validators=[MaxValueValidator(240),
                    MinValueValidator(1)],
        blank=False,
        default=1,
        verbose_name='Время приготовленмя')


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
    amount = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество ингредиентор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique ingredient per recipe'
            ), ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')


class Shopping(models.Model):
    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')

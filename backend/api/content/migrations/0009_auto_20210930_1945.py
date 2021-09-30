# Generated by Django 3.2 on 2021-09-30 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20210927_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredientrecipe', to='content.ingredient', verbose_name='Ингредиент в рецепте'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='user_api/', verbose_name='Изображение'),
        ),
    ]

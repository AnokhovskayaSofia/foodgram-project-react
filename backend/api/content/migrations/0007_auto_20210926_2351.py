# Generated by Django 3.2 on 2021-09-26 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_ingredientsrecipe_unique ingredient per recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_content', to='content.ingredient', verbose_name='Ингредиент в рецепте'),
        ),
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_content', to='content.recipe', verbose_name='Рецепт'),
        ),
    ]

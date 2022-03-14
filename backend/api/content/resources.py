from import_export import resources

from .models import (Favourite, Ingredient, IngredientsRecipe, Recipe,
                     Shopping, Tag)


class RecipeResource(resources.ModelResource):
    class Meta:
        model = Recipe
        fields = ('id',
                  'author',
                  'name',
                  'text',
                  'ingredients',
                  'tags',
                  'cooking_time',)


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeResource(resources.ModelResource):
    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'ingredient', 'recipe', 'amount')


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
        fields = ('id', 'HEX_code', 'slug',)


class FavouriteResource(resources.ModelResource):
    class Meta:
        model = Favourite
        fields = ('id', 'user', 'recipe',)


class ShoppingResource(resources.ModelResource):
    class Meta:
        model = Shopping
        fields = ('id', 'user', 'recipe',)

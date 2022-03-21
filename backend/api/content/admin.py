from django.contrib import admin
from import_export.admin import ImportMixin # type: ignore

from .models import (Favourite, Ingredient, IngredientsRecipe, Recipe,
                     Shopping, Tag)
from .resources import (FavouriteResource, IngredientResource,
                        IngredientsRecipeResource, RecipeResource,
                        ShoppingResource, TagResource)


class RecipeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = RecipeResource


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = IngredientResource


class IngredientsRecipeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = IngredientsRecipeResource


class TagAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = TagResource


class FavouriteAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = FavouriteResource


class ShoppingAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ShoppingResource


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientsRecipe, IngredientsRecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Shopping, ShoppingAdmin)

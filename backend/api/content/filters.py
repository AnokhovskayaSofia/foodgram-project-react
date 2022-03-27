from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Ingredient, Recipe
from .serializer import GetRecipeSerializer


class RecipeFilter(FilterSet):
    author = filters.AllValuesFilter(field_name='author')
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = filters.AllValuesMultipleFilter(field_name='recipes__tags__slug')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(favourite__user=user)
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        shopping = Recipe.objects.filter(shoppings__user=user)
        if value:
            # page = self.paginate_queryset(shopping)
            # if page is not None:
                # serializer = GetRecipeSerializer(page, many=True)
                # return self.get_paginated_response(serializer.data)
            return Recipe.objects.filter(shoppings__user=user)
        return Recipe.objects.all()

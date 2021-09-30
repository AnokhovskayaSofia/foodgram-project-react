from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Recipe


class RecipeFilter(FilterSet):
    author = filters.AllValuesFilter(field_name='author')
    is_favorited = filters.ModelChoiceFilter(queryset=Recipe.objects.all(),
                                             method='filter_is_favorited')
    is_in_shopping_cart = filters.ModelChoiceFilter(queryset=Recipe.objects.all(),
                                                    method='filter_is_in_shopping_cart')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(favorite__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(shopping__user=self.request.user)

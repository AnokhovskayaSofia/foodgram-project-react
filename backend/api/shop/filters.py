from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Ingredient, Product
from .serializer import GetProductSerializer


class ProductFilter(FilterSet):
    author = filters.AllValuesFilter(field_name='author')

    # is_in_shopping_cart = filters.BooleanFilter(
    #     method='get_is_in_shopping_cart'
    # )
    item = filters.AllValuesMultipleFilter(field_name='item__slug')

    class Meta:
        model = Product
        # fields = ['is_in_shopping_cart', 'author', 'item']
        fields = ['author', 'item']

    # def get_is_in_shopping_cart(self, queryset, name, value):
    #     user = self.request.user
    #     shopping = Product.objects.filter(shoppings__user=user)
    #     if value:
    #         # page = self.paginate_queryset(shopping)
    #         # if page is not None:
    #             # serializer = GetRecipeSerializer(page, many=True)
    #             # return self.get_paginated_response(serializer.data)
    #         return Product.objects.filter(shoppings__user=user)
    #     return Product.objects.all()
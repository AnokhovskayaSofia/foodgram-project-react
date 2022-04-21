from django_filters import filters
from django_filters.rest_framework import FilterSet

# from .models import Ingredient, MyProduct
# from .serializer import GetProductSerializer


# class ProductFilter(FilterSet):
#     author = filters.AllValuesFilter(field_name='author')

#     is_in_shopping_cart = filters.BooleanFilter(
#         method='get_is_in_shopping_cart'
#     )
#     item = filters.AllValuesMultipleFilter(field_name='item__slug')

#     class Meta:
#         model = MyProduct
#         fields = ['is_in_shopping_cart', 'author', 'item']

#     def get_is_in_shopping_cart(self, queryset, name, value):
#         user = self.request.user
#         shopping = MyProduct.objects.filter(shoppings__user=user)
#         if value:
#             # page = self.paginate_queryset(shopping)
#             # if page is not None:
#                 # serializer = GetRecipeSerializer(page, many=True)
#                 # return self.get_paginated_response(serializer.data)
#             return MyProduct.objects.filter(shoppings__user=user)
#         return MyProduct.objects.all()
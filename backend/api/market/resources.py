from import_export import resources

from .models import (Item , Product, ShoppingCart)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'text',
                  'item',)

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ('id', 'HEX_code', 'slug',)


# class ShoppingCartResource(resources.ModelResource):
#     class Meta:
#         model = ShoppingCart
#         fields = ('user', 'product', 'count',)

from import_export import resources

from .models import (Item, MyProduct, ShoppingCart)


class ProductResource(resources.ModelResource):
    class Meta:
        model = MyProduct
        fields = ('id',
                  'name',
                  'text',
                  'item',
                  'price',)

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ('id', 'HEX_code', 'slug',)


class ShoppingCartResource(resources.ModelResource):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'count',)

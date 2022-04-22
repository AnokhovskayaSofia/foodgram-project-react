from django.contrib import admin
from import_export.admin import ImportMixin

from market.models import Item
from market.resources import ItemResource
# from market.models import (Item, MyProduct, ShoppingCart)
# from market.resources import (ProductResource, ItemResource, ShoppingCartResource)


# class ProductAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = ProductResource

class ItemAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ItemResource

# class ShoppingCartAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = ShoppingCartResource

# admin.site.register(MyProduct, ProductAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(ShoppingCart, ShoppingCartAdmin)
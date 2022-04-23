from django.contrib import admin
from import_export.admin import ImportMixin

from shop.models import (Item, Product, ShoppingCart, Cart)
from shop.resources import (ProductResource, ItemResource, ShoppingCartResource, CartResource)


class ProductAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ProductResource

class ItemAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ItemResource

# class ShoppingCartAdmin(ImportMixin, admin.ModelAdmin):
#     resource_class = ShoppingCartResource

class CartAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = CartResource

admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Cart, CartAdmin)

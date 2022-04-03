from django.contrib import admin
from import_export.admin import ImportMixin

from market.models import (Item, Product)
from market.resources import (ProductResource, ItemResource)


class ProductAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ProductResource

class ItemAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ItemResource

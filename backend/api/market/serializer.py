from django.db.models import F
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

# from users.serializers import UserSerializer

from .models import (Item, MyProduct)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Item

class GetProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    item = ItemSerializer(many=True, read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = MyProduct
        fields = ('id',
                  'item',
                  'name',
                  'image',
                  'price',
                  'text',)


class ShortProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    image = serializers.ImageField()
    price = serializers.DecimalField(max_digits=4,
                                     decimal_places=1)

    class Meta:
        model = MyProduct
        fields = ('id',
                  'name',
                  'image',
                  'price',)
from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import (Item, Product)
from .serializer import (ItemSerializer, GetProductSerializer)



class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = PageNumberPagination.page_size = 999
    pagination_class = PageNumberPagination
    # filter_backends = (DjangoFilterBackend,)
    # filter_class = RecipeFilter
    # filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags__slug', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return GetProductSerializer

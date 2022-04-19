from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.colors import blue, black, grey
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import (Item, Product, ShoppingCart)
from .serializer import (ItemSerializer, GetProductSerializer, ShortProductSerializer)



class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None



class ProductViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = GetProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = PageNumberPagination.page_size = 999
    pagination_class = PageNumberPagination
    # filter_backends = (DjangoFilterBackend,)
    # filter_class = RecipeFilter
    # filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags__slug', )

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return GetProductSerializer

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated],
            pagination_class = None,
            url_path='product_cart')
    def product_cart(self, request, pk=None):
        if request.method == 'GET':
            product = get_object_or_404(Product, pk=pk)
            serializer = ShortProductSerializer(product)
            if ShoppingCart.objects.filter(user=self.request.user,
                                       product=product).exists():
                return Response({'errors': 'Продукт уже в Списке покупок'})
            else:
                ShoppingCart.objects.create(user=self.request.user,
                                        product=product)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            product = get_object_or_404(Product, pk=pk)
            if ShoppingCart.objects.filter(user=self.request.user,
                                       product=product).exists():
                instance = ShoppingCart.objects.get(user=self.request.user,
                                                product=product)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'errors': 'Продукта нет в Списке покупок'},
                                 status=status.HTTP_400_BAD_REQUEST)

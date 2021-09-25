from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .permissions import CustomPermissions
from .serializer import RecipeSerializer, IngredientsSerializer, TagsSerializer
from .models import Recipe, Ingredient, Tag

PERMISSIONS = [IsAuthenticatedOrReadOnly, CustomPermissions]

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permission_classes = PERMISSIONS
    # pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    
    print('RecipeViewSet')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, )

class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    # permission_classes = PERMISSIONS
    # pagination_class = None
    # filterset_fields = ['name']
    # filter_backends = [filters.SearchFilter]
    
    print('IngredientsViewSet')


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    # permission_classes = PERMISSIONS
    # pagination_class = None
    # filterset_fields = ['id']
    # filter_backends = [filters.SearchFilter]
    
    print('viewsetTag')



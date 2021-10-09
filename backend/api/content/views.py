from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import (Favourite, Ingredient, IngredientsRecipe, Recipe,
                     Shopping, Tag)
from .serializer import (GetRecipeSerializer, IngredientSerializer,
                         PostRecipeSerializer, ShortRecipeSerializer,
                         TagsSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return PostRecipeSerializer

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated],
            url_path='favorite')
    def favorite(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, pk=pk)
            serializer = ShortRecipeSerializer(recipe)
            if Favourite.objects.filter(user=self.request.user,
                                        recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже в Избранном'})
            else:
                Favourite.objects.create(user=self.request.user, recipe=recipe)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            if Favourite.objects.filter(user=self.request.user,
                                        recipe=recipe).exists():
                instance = Favourite.objects.get(user=self.request.user,
                                                 recipe=recipe)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'errors': 'Рецепта нет в Избранном'},
                                 status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['GET', 'DELETE'],
            permission_classes=[IsAuthenticated],
            url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, pk=pk)
            serializer = ShortRecipeSerializer(recipe)
            if Shopping.objects.filter(user=self.request.user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже в Списке покупок'})
            else:
                Shopping.objects.create(user=self.request.user,
                                        recipe=recipe)
            return Response(serializer.data)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            if Shopping.objects.filter(user=self.request.user,
                                       recipe=recipe).exists():
                instance = Shopping.objects.get(user=self.request.user,
                                                recipe=recipe)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'errors': 'Рецепта нет в Списке покупок'},
                                 status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        all_ingredients_amount = IngredientsRecipe.objects.filter(
            recipe__shoppings__user=request.user).values_list(
                'ingredient__name', 'amount',
                'ingredient__measurement_unit')
        sum_amount_ingredient = all_ingredients_amount.values(
                                'ingredient__name',
                                'ingredient__measurement_unit').annotate(
                                total=Sum('amount')).order_by('-total')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping.pdf"'
        p = canvas.Canvas(response)
        line_position = 800
        for recipes_item in sum_amount_ingredient:
            data = str(recipes_item)
            line_position -= 15
            p.drawString(10, line_position, data)
        p.showPage()
        p.save()
        return response


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    filter_backends = (filters.SearchFilter) 
    search_fields = ('^name',)

    def list(self,request):
          serializer = IngredientSerializer(self.get_queryset(), many=True)
          return Response(serializer.data)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.colors import blue, black
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

from .filters import RecipeFilter
from .models import (Favourite, Ingredient, IngredientsRecipe, Recipe,
                     Shopping, Tag)
from .serializer import (GetRecipeSerializer, IngredientSerializer,
                         PostRecipeSerializer, ShortRecipeSerializer,
                         TagsSerializer)


class CustomPageNumberPaginator(PageNumberPagination):
    page_size_query_param = 'limit'

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GetRecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = PageNumberPagination.page_size = 999
    pagination_class = CustomPageNumberPaginator
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
            pagination_class = None,
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
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping.pdf"'
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('DejaVuSans','DejaVuSans.ttf', 'UTF-8'))
        pdfmetrics.registerFont(TTFont('Arial','Arial.ttf', 'UTF-8'))

        res = []
        
        rec_ingredients = (
                IngredientsRecipe.objects.values(
                    'ingredient__name',
                    'ingredient__measurement_unit',
                )
                .filter(recipe__shoppings__user=request.user)
                .annotate(Sum('amount'))
            )
        for rec_ingredient in rec_ingredients:
            res.append(
                f"{rec_ingredient['ingredient__name'].capitalize()} - "
                f"{rec_ingredient['amount__sum']} "
                f"{rec_ingredient['ingredient__measurement_unit']}"
            )

        line_position = 800
        title = f"Список покупок для рецептов:"
        p.setFont("Arial", 20)
        p.setFillColor(blue)
        p.drawString(30, line_position, title)
        

        p.setFont("DejaVuSans", 10)
        p.setFillColor(black)
        line_position -= 15
        for recipes_item in res:
            data = str(recipes_item)
            line_position -= 15
            p.drawString(35, line_position, data)
        
        p.showPage()
        p.save()
        return response


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def list(self,request):
          serializer = IngredientSerializer(self.get_queryset(), many=True)
          return Response(serializer.data)
    
    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = Ingredient.objects.all()

        if name:
            queryset = queryset.filter(name__istartswith=name).distinct('name')

        return queryset


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from .serializer import RecipeSerializer, ShortRecipeSerializer, IngredientSerializer, TagsSerializer
from .models import Recipe, Ingredient, Tag, Favourite, Shopping, IngredientsRecipe
from .filters import RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

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
        user = self.request.user
        shopping_list = Shopping.objects.filter(user=user)
        recipes_querysets = []
        for item in shopping_list:
            recipes_querysets.append(
                item.recipe.recipe_content.values_list(
                    'ingredient__name',
                    'amount',
                    'ingredient__measurement_unit')
                )
        # print(recipes_querysets)
        recipes_list = {}
        for recipes_item in recipes_querysets:
            for item in recipes_item:
                if not item[0] in recipes_list:
                    recipes_list[item[0]] = {
                        'amount': item[1], 'measurement_unit': item[2]
                    }
                else:
                    recipes_list[item[0]]['amount'] += item[1]

        data = recipes_list
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shoppinglist.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 100, data)
        # p.showPage()
        # p.save()
        return response


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    filter_backends = (filters.SearchFilter)
    search_fields = ('^name',)


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='RecipeViewSet')
router.register('tags', TagsViewSet, basename='TagsViewSet')
router.register('ingredients', IngredientsViewSet,
                basename='IngredientsViewSet')

urlpatterns = [
    path('', include(router.urls)),
]

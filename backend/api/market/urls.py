from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register('product', ProductViewSet, basename='ProductViewSets')
router.register('item', ItemViewSet, basename='ItemViewSet')

urlpatterns = [
    path('', include(router.urls)),
]
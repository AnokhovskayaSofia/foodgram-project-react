from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()
router.register('product', ProductViewSet, basename='ProductViewSets')

urlpatterns = [
    path('', include(router.urls)),
]
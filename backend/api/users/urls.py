from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import UserViewSet, activate, signup

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # path('/', include(router.urls)),
    # path('email/', signup, name='signup'),
    # path('token/', activate, name='activate'),
    path('', include('djoser.urls')),
]

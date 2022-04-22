from django.contrib import admin
from django.urls import include, path
from djoser import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('content.urls')),
    path('api/', include('market.urls')),
    path('api/', include('shop.urls')),
    path('api/auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('api/auth/token/logout/', views.TokenDestroyView.as_view(), name='logout')
]

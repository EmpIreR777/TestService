from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

from .views import CategoryViewSet, ProductViewSet


v1_router = DefaultRouter()

v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger'),
]

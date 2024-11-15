from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

from .views import CategoryViewSet


v1_router = DefaultRouter()

v1_router.register(r'category', CategoryViewSet, basename='category')


urlpatterns = [
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    path('', include(v1_router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger'),
]

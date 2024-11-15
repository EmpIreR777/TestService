from rest_framework.viewsets import ModelViewSet

from review.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """Просмотр всех категорий с подкатегориями."""

    # permission_classes = (.)
    # http_method_names = ('get', 'post', 'patch', 'delete')
    # pagination_class = PagePagination
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(
            parent__isnull=True).prefetch_related('children')
    


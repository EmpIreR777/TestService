from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from review.models import Category, Product, ShoppingCart
from .serializers import (CategorySerializer,
                          ProductSerializer,
                          ShoppingCartSerializer,
                          CartSerializer)


class CategoryViewSet(ModelViewSet):
    """Просмотр всех категорий с подкатегориями."""

    # permission_classes = (.)
    # http_method_names = ('get', 'post', 'patch', 'delete')
    # pagination_class = PagePagination
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(
            parent__isnull=True).prefetch_related('children')


class ProductViewSet(ModelViewSet):
    """Просмотр всех продуктов."""

    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]

    @staticmethod
    def add_method(serializer_cls, request, pk):
        if not Product.objects.filter(id=pk).exists():
            return Response(
                data={'error': 'Вы пытаетесь добавить несуществующий продукт'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        cart_item, created = ShoppingCart.objects.get_or_create(
            user=request.user,
            product_id=pk,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = serializer_cls(
            cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete_method(model, request, pk):
        if not Product.objects.filter(id=pk).exists():
            return Response(
                data={'error': 'Вы пытаетесь удалить несуществующий продукт'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            cart_item = model.objects.get(user=request.user, product_id=pk)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                return Response(
                    {'quantity': cart_item.quantity},
                    status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except model.DoesNotExist:
            return Response({'error': 'Нет в добавленных.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self.add_method(ShoppingCartSerializer, request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method(ShoppingCart, request, pk)

    @action(methods=('get',), detail=False,
            permission_classes=(IsAuthenticated,))
    def list_shopping_cart(self, request):
        serializer = CartSerializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthenticated])
    def clear(self, request):
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

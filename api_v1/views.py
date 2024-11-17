from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from review.models import Category, Product, ShoppingCart
from .permissions import IsOwnerOfCart
from .serializers import (CategorySerializer,
                          ProductSerializer,
                          ShoppingCartSerializer,
                          PutShoppingCartSerializer,
                          CartSerializer)


class CategoryViewSet(ReadOnlyModelViewSet):
    """Просмотр всех категорий с подкатегориями."""

    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.filter(
            parent__isnull=True).prefetch_related('children')


class ProductViewSet(ReadOnlyModelViewSet):
    """Просмотр всех продуктов."""

    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

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
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = serializer_cls(
            cart_item, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete_method(model, request, pk):
        model.objects.filter(
            user=request.user, product_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def put_method(serializer_cls, request, pk):
        serializer = serializer_cls(data=request.data)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.filter(
            user=request.user, product_id=pk).update(
                quantity=serializer.data['quantity'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=('put',),
        permission_classes=(IsOwnerOfCart,),serializer_class=PutShoppingCartSerializer
    )
    def put_shopping_cart(self, request, pk):
        return self.put_method(PutShoppingCartSerializer, request, pk)

    @action(detail=True, methods=('post',),
            permission_classes=(IsOwnerOfCart,),
            serializer_class=None)
    def shopping_cart(self, request, pk):
        return self.add_method(ShoppingCartSerializer, request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method(ShoppingCart, request, pk)

    @action(methods=('get',), detail=False,
            permission_classes=(IsOwnerOfCart,))
    def list_shopping_cart(self, request):
        serializer = CartSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=('delete',),
            permission_classes=(IsOwnerOfCart,))
    def clean_shopping_cart(self, request):
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

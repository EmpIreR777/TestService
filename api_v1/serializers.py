from rest_framework import serializers
from django.contrib.auth import get_user_model

from review.models import Category, Product, ShoppingCart


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализации объектов модели Category и её иерархии."""

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['title', 'slug', 'image', 'children']

    def get_children(self, obj):
        children = obj.children.all()
        if not children.exists():
            return None
        return CategorySerializer(children, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['children'] is None:
            representation.pop('children')
        return representation


class ProductSerializer(serializers.ModelSerializer):
    """Сериализации объектов продуктов."""

    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'title', 'slug',
            'price', 'image',
            'category',
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор отдельного элемента корзины."""

    product = serializers.StringRelatedField()

    class Meta:
        model = ShoppingCart
        fields = ('product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины пользователя."""

    products = ShoppingCartSerializer(
        source='shopping_carts', many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['products', 'total_quantity', 'total_price']

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.shopping_carts.all())

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity
                   for item in obj.shopping_carts.all())

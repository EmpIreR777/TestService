from rest_framework import serializers
from django.contrib.auth import get_user_model

from versatileimagefield.serializers import VersatileImageFieldSerializer
from review.models import Category, Product, ShoppingCart


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализации объектов модели Category и её иерархии."""

    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title',
                  'slug', 'image',
                  'children'
                  ]

    def get_children(self, obj):
        children = obj.children.all()
        return CategorySerializer(children, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    """Сериализации объектов продуктов."""

    category = CategorySerializer()
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__300x300'),
        ]
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title', 'slug',
            'price', 'image',
            'category',
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор отдельного элемента корзины."""

    product = ProductSerializer()

    class Meta:
        model = ShoppingCart
        fields = ('product', 'quantity')


class PutShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор отдельного элемента корзины."""

    class Meta:
        model = ShoppingCart
        fields = ('quantity',)


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

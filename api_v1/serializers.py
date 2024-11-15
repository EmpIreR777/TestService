from rest_framework import serializers

from review.models import Category, Product, ShoppingCart


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
    """Сериализатор корзины."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'quantity')


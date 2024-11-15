from rest_framework import serializers

from review.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализации объектов модели Category и её иерархии."""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', 'children']

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

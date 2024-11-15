from rest_framework import serializers

from review.models import Category


class RecursiveField(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(
            value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image', 'children']

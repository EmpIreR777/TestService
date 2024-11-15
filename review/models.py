from django.db import models
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Модель категорий с вложеностью."""
    title = models.CharField(
        'Название категории', max_length=255
    )
    slug = models.SlugField(
        'Слаг категории', max_length=255
    )
    image = models.ImageField(
        'Изображение рецепта', upload_to='media/category',
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        db_index=True, related_name='children',
        verbose_name='Родительская категория',
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        return self.title

    # Можем убрать метод что бы у нас было множественное наследование 
    def clean(self):
        if self.parent:
            if self.parent.parent is not None:
                raise ValidationError('Подкатегория может быть только дочерней к верхнеуровневой категории.')
            existing_children = Category.objects.filter(parent=self.parent).exclude(pk=self.pk)
            if existing_children.exists():
                raise ValidationError('Каждая категория может иметь только одну подкатегорию.')

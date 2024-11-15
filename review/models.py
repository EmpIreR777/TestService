from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Модель категорий с вложеностью."""

    title = models.CharField(
        'Название категории',
        max_length=255,
        help_text='Добавьте название.',
    )
    slug = models.SlugField(
        'Слаг категории',
        max_length=255,
        unique=True,
        help_text='Добавьте слаг.',
    )
    image = models.ImageField(
        'Изображение категории',
        upload_to='category/',
        help_text='Добавьте изображение.',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория',
        help_text='Добавьте родительскую категорию.',
    )
    is_published = models.BooleanField(
        'Публикация продукта',
        default=False,
        help_text='Нажмите на если хотите опубликовать категорию.',
    )
    publish = models.DateTimeField(
        'Дата публикации', default=timezone.now()
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    # Можем убрать проверку, что бы у нас было множественное наследование
    def clean(self):
        if self.parent and self.parent.parent is not None:
            raise ValidationError('Подкатегория может быть только дочерней к верхнеуровневой категории.')
        existing_children = Category.objects.filter(parent=self.parent).exclude(pk=self.pk)
        if not self.image:
            raise ValidationError('Изображение категории обязательно.')


class Product(models.Model):
    """Модель продуктов."""

    title = models.CharField(
        'Название продуктов',
        max_length=255,
        help_text='Добавьте название.',
    )
    slug = models.SlugField(
        'Слаг продуктов',
        max_length=255,
        unique=True,
        help_text='Добавьте слаг.',
    )
    image = models.ImageField(
        'Изображение продуктов',
        upload_to='product/',
        help_text='Добавьте изображение.',
    )
    price = models.DecimalField(
        'Цена продукта',
        max_digits=10,
        decimal_places=2,
        help_text='Введите цену.',
    )
    is_published = models.BooleanField(
        'Публикация продукта',
        default=False,
        help_text='Нажмите на если хотите опубликовать продукт.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        help_text='Выберите категорию, к которой относится продукт.',
    )
    description = models.TextField(
        'Описание продукта', max_length=555
    )
    publish = models.DateTimeField(
        'Дата публикации', default=timezone.now()
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True
    )
    updated = models.DateTimeField(
        'Дата обновления', auto_now=True
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

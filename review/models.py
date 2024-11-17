from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from versatileimagefield.fields import VersatileImageField, PPOIField
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()


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
        blank=True, null=True
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
        'Публикация категории',
        default=False,
        help_text='Нажмите на если хотите опубликовать категорию.',
    )
    publish = models.DateTimeField(
        'Дата публикации', default=timezone.now
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


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
    image = VersatileImageField(
        'Изображение продуктов',
        upload_to='product/',
        ppoi_field='image_ppoi',
        help_text='Добавьте изображение.',
        blank=True, null=True,
    )
    image_ppoi = PPOIField()
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
        limit_choices_to={'parent__isnull': False},
        help_text='Выберите категорию, к которой относится продукт.',
    )
    description = models.TextField(
        'Описание продукта'
    )
    publish = models.DateTimeField(
        'Дата публикации', default=timezone.now
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True,
    )
    updated = models.DateTimeField(
        'Дата обновления', auto_now=True,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_carts',
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name='Продукт',
        related_name='shopping_carts',
    )
    quantity = models.PositiveIntegerField(
        'Количество', default=1,
    )

    class Meta:
        unique_together = ('user', 'product')
        default_related_name = 'shopping_carts'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

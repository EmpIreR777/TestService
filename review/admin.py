from django.contrib import admin
from django.utils.html import format_html

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, ShoppingCart


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Админ-панель модели категорий."""

    list_filter = ('title', 'slug')
    search_fields = ('slug',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'indented_title',
        'tree_actions',
        'show_image',
        'slug',
    )

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;"/>',
                obj.image.url)
        return 'Нет изображения'

    show_image.short_description = 'Изображение'


@admin.action(description='Снять с публикации')
def published_false(modelAdmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description='Поставить на публикацию')
def published_true(modelAdmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель модели Продуктов."""

    actions = [
        published_true,
        published_false,
    ]
    list_filter = ('title', 'slug', 'category')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('id', 'title')
    list_display = (
        'id',
        'title',
        'slug',
        'show_image',
        'price',
        'category',
    )

    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;"/>',
                obj.image.url)
        return 'Нет изображения'

    show_image.short_description = 'Изображение'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ-панель модели корзина."""

    list_filter = (
        'product',
    )
    list_display = ('user', 'product', 'quantity')


admin.site.empty_value_display = 'Не задано'
admin.site.site_header = 'Sarafan-shop'
admin.site.index_title = 'Админ панель магазина продуктов - Sarafan-shop'

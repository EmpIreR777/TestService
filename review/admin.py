from django.contrib import admin
from django.utils.html import format_html

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product, ShoppingCart


@admin.action(description='Снять с публикации')
def published_false(modelAdmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description='Поставить на публикацию')
def published_true(modelAdmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Админ-панель модели категорий."""

    actions = [
            published_true,
            published_false,
        ]
    list_filter = (
        'title', 'slug'
    )
    search_fields = (
        'slug',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_display = (
        'id',
        'indented_title',
        'tree_actions',
        'show_image',
        'slug',
    )

    @admin.display(description='Изображение')
    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;"/>',
                obj.image.url)
        return format_html('<img src="{}" style="width: 90px; height: 55px;"/>', '/media/category/default.jpg')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель модели продуктов."""

    actions = [
        published_true,
        published_false,
    ]
    list_filter = (
        'title', 'slug', 'category',
    )
    search_fields = (
        'title', 'slug',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_display_links = (
        'id', 'title'
    )
    list_display = (
        'id',
        'title',
        'slug',
        'show_image',
        'price',
        'category',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category')

    @admin.display(description='Изображение')
    def show_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;"/>',
                obj.image.url)
        return format_html('<img src="{}" style="width: 90px; height: 55px;"/>', '/media/product/default.jpg')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ-панель модели корзина."""

    list_filter = (
        'user',
        'product',
    )
    list_display = (
        'user', 'product',
        'quantity', 'get_price'
    )
    list_editable = ('quantity',)
    list_display_links = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('product')

    @admin.display(description='Стоимость')
    def get_price(self, obj):
        total_price = obj.product.price * obj.quantity
        return f'{total_price} ₽'


admin.site.site_header = 'Sarafan-shop'
admin.site.index_title = 'Админ панель магазина продуктов - Sarafan-shop'
admin.site.empty_value_display = 'Не задано'

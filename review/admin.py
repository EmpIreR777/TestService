from django.contrib import admin
from django.utils.html import format_html

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Продуктов
    """

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

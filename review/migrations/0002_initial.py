# Generated by Django 4.2 on 2024-11-17 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию, к которой относится продукт.', limit_choices_to={'parent__isnull': False}, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='review.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, help_text='Добавьте родительскую категорию.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='review.category', verbose_name='Родительская категория'),
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together={('user', 'product')},
        ),
    ]

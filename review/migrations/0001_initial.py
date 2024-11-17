# Generated by Django 4.2 on 2024-11-17 09:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Добавьте название.', max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Добавьте слаг.', max_length=255, unique=True, verbose_name='Слаг категории')),
                ('image', models.ImageField(help_text='Добавьте изображение.', upload_to='category/', verbose_name='Изображение категории')),
                ('is_published', models.BooleanField(default=False, help_text='Нажмите на если хотите опубликовать категорию.', verbose_name='Публикация категории')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Добавьте название.', max_length=255, verbose_name='Название продуктов')),
                ('slug', models.SlugField(help_text='Добавьте слаг.', max_length=255, unique=True, verbose_name='Слаг продуктов')),
                ('image', models.ImageField(blank=True, help_text='Добавьте изображение.', null=True, upload_to='product/', verbose_name='Изображение продуктов')),
                ('price', models.DecimalField(decimal_places=2, help_text='Введите цену.', max_digits=10, verbose_name='Цена продукта')),
                ('is_published', models.BooleanField(default=False, help_text='Нажмите на если хотите опубликовать продукт.', verbose_name='Публикация продукта')),
                ('description', models.TextField(max_length=555, verbose_name='Описание продукта')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to='review.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'default_related_name': 'shopping_carts',
            },
        ),
    ]

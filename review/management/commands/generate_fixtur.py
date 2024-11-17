import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from review.models import Category, Product


fake = Faker()


class Command(BaseCommand):
    help = 'Генерация данных для базы данных'

    def handle(self, *args, **kwargs):
        top_categories = []
        subcategories = []
        for _ in range(10):
            title = fake.unique.word().capitalize()
            slug = slugify(title)
            category = Category(title=title, slug=slug, is_published=True, publish=fake.date_time_this_year())
            top_categories.append(category)

            for _ in range(random.randint(1, 3)):
                sub_title = fake.unique.word().capitalize()
                sub_slug = slugify(sub_title)
                subcategory = Category(
                    title=sub_title,
                    slug=sub_slug,
                    parent=category,
                    is_published=True,
                    publish=fake.date_time_this_year(),
                )
                subcategories.append(subcategory)

        Category.objects.bulk_create(top_categories + subcategories)

        all_subcategories = list(Category.objects.filter(parent__isnull=False))
        products = []
        for _ in range(50):
            title = fake.unique.word().capitalize()
            slug = slugify(title)
            category = random.choice(all_subcategories)
            product = Product(
                title=title,
                slug=slug,
                price=round(random.uniform(10.0, 1000.0), 2),
                is_published=True,
                category=category,
                description=fake.text(max_nb_chars=500),
                publish=fake.date_time_this_year(),
            )
            products.append(product)

        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS('Данные успешно сгенерированы'))

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from review.models import Category, Product


User = get_user_model()


class ProductApiTests(APITestCase):
    """Get запросы для продуктов и категорий."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'testuser'
        cls.password = 'testpassword'
        cls.email = 'testemail@mail.com'
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
            email=cls.email)
        cls.category = Category.objects.create(title='Категория 1', slug='category-1', is_published=True)
        cls.sub_category = Category.objects.create(title='Саб Категория 1', slug='sub-category-1', is_published=True, parent=cls.category)
        cls.product = Product.objects.create(
            title='Новый продукт',
            slug='new-product',
            price='99.99',
            is_published=True,
            category=cls.sub_category,
            description='Описание нового продукта',
        )

    def test_get_products(self):
        """
        Протестируйте добавление товара в корзину покупок.
        """
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'title': 'Новый продукт',
                    'slug': 'new-product',
                    'price': '99.99',
                    'image': {},
                    'category': {
                        'id': 2,
                        'title': 'Саб Категория 1',
                        'slug': 'sub-category-1',
                        'image': None,
                        'children': [],
                    },
                }
            ],
        }
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_get_categories(self):
        """
        Попробуйте удалить товар из корзины покупок.
        """
        expected = [
            {
                'id': 1,
                'title': 'Категория 1',
                'slug': 'category-1',
                'image': None,
                'children': [
                    {'id': 2, 'title': 'Саб Категория 1', 'slug': 'sub-category-1', 'image': None, 'children': []}
                ],
            }
        ]
        url = reverse('categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected)


class UserRegistrationAndAuthApiTests(APITestCase):
    """Регистрация и получение токина."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'testuser'
        cls.password = 'testpassword'
        cls.email = 'testemail@mail.com'
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
            email=cls.email)

    def test_jwt_authentication_success(self):
        """
        Проверяет успешную аутентификацию пользователя и получение JWT-токенов.
        """
        payload = {
            'username': self.username,
            'password': self.password
            }
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_authentication_failure_wrong_password(self):
        """
        Проверяет неуспешную аутентификацию с неправильным паролем.
        """
        payload = {
            'username': self.username,
            'password': 'failpassword'
            }
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_jwt_token_refresh(self):
        """
        Проверяет обновление JWT-токена с помощью refresh-токена.
        """
        payload = {
            'username': self.username,
            'password': self.password
            }
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']
        refresh_payload = {'refresh': refresh_token}
        refresh_response = self.client.post('/auth/jwt/refresh/', refresh_payload)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

"""Здесь я, вместо использования reverse, использую явное указание URL пути. На мой взгляд, при использовании reverse, тесты все равно пройдут, если кто-то случайно изменил url путь, но frontend часть проекта перестанет работать. Также, возможен вариант использования здесь reverse, но написать отдельные тесты, которые будут проверять то, что результат выполнения reverse для разных url путей не изменился."""

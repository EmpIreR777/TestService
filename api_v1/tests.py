from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from review.models import Category, Product


User = get_user_model()


class ProductAPITests(APITestCase):

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
        cls.mock_image = SimpleUploadedFile(
            name='image.jpeg', content=b'x47x49x46x38x39x61', content_type='image/jpeg'
        )
        cls.product = Product.objects.create(
            title='Новый продукт',
            slug='new-product',
            price='99.99',
            is_published=True,
            category=cls.category,
            description='Описание нового продукта',
            image=cls.mock_image,
        )
        cls.client.login(username=cls.username, password=cls.password)

    def test_add_product_to_cart(self):
        """
        Протестируйте добавление товара в корзину покупок.
        """
        url = reverse('product-shopping_cart', kwargs={'id': self.product.id})
        with mock.patch('review.models.Product.image', return_value=self.mock_image):
            response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data.get('message', '').lower())

        # self.assertTrue(self.user.cart.products.filter(id=self.product.id).exists())

    def test_remove_product_from_cart(self):
        """
        Попробуйте удалить товар из корзины покупок.
        """
        self.client.post('/api/product/{id}/shopping_cart/' , format='json')
        response = self.client.delete('/api/product/{id}/shopping_cart/',format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('removed', response.data.get('message', '').lower())
        # self.assertFalse(self.user.cart.products.filter(id=self.product.id).exists())


# class UserRegistrationAndAuthTests(APITestCase):
#     """Регистрация и получение токина."""

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.username = 'testuser'
#         cls.password = 'testpassword'
#         cls.email = 'testemail@mail.com'
#         cls.user = User.objects.create_user(
#             username=cls.username,
#             password=cls.password,
#             email=cls.email)

#     def test_jwt_authentication_success(self):
#         """
#         Проверяет успешную аутентификацию пользователя и получение JWT-токенов.
#         """
#         payload = {
#             'username': self.username,
#             'password': self.password
#             }
#         response = self.client.post('/auth/jwt/create/', payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', response.data)
#         self.assertIn('refresh', response.data)

#     def test_jwt_authentication_failure_wrong_password(self):
#         """
#         Проверяет неуспешную аутентификацию с неправильным паролем.
#         """
#         payload = {
#             'username': self.username,
#             'password': 'failpassword'
#             }
#         response = self.client.post('/auth/jwt/create/', payload)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

#     def test_jwt_token_refresh(self):
#         """
#         Проверяет обновление JWT-токена с помощью refresh-токена.
#         """
#         payload = {
#             'username': self.username,
#             'password': self.password
#             }
#         response = self.client.post('/auth/jwt/create/', payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         refresh_token = response.data['refresh']

#         refresh_payload = {'refresh': refresh_token}
#         refresh_response = self.client.post('/auth/jwt/refresh/', refresh_payload)
#         self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', refresh_response.data)

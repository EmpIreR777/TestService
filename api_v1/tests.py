from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationAndAuthTests(APITestCase):
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
        payload = {'username': self.username, 'password': self.password}
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_authentication_failure_wrong_password(self):
        """
        Проверяет неуспешную аутентификацию с неправильным паролем.
        """
        payload = {'username': self.username, 'password': 'failpassword'}
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_jwt_token_refresh(self):
        """
        Проверяет обновление JWT-токена с помощью refresh-токена.
        """
        payload = {'username': self.username, 'password': self.password}
        response = self.client.post('/auth/jwt/create/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        refresh_payload = {'refresh': refresh_token}
        refresh_response = self.client.post('/auth/jwt/refresh/', refresh_payload)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

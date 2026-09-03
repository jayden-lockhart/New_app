from accounts.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

class AuthenticatedTokenAccessTest(APITestCase):
    def setUp(self):
        """
        Create a test user and generate an authentication token.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="securepassword123"
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": f"Token {self.token.key}"
        }
        self.url = "/api/protected-endpoint/"  # Replace with your endpoint

    def test_access_with_valid_token(self):
        """
        Ensure that a valid token grants access.
        """
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_without_token(self):
        """
        Ensure that no token returns 401 Unauthorized.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        """
        Ensure that an invalid token returns 401 Unauthorized.
        """
        invalid_headers = {
            "HTTP_AUTHORIZATION": "Token invalidtoken123"
        }
        response = self.client.get(self.url, **invalid_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

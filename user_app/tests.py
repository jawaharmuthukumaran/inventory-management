from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterTests(APITestCase):
    def setUp(self):
        # URL paths for registration, login, and token refresh
        self.register_url = reverse("register")
        self.login_url = reverse("login")

        # Set up admin and regular user data
        self.admin_user_data = {"username": "adminuser", "password": "adminpassword"}
        self.test_user_data = {"username": "testuser", "password": "testpassword123"}

        # Create an admin user
        self.admin_user = User.objects.create_superuser(**self.admin_user_data)

    def get_admin_token(self):
        # Obtain JWT token for admin user
        response = self.client.post(self.login_url, self.admin_user_data)
        return response.data["access"]

    def test_user_registration_with_admin(self):
        # Obtain JWT token for the admin user
        admin_token = self.get_admin_token()

        # Set the JWT token in the request headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")

        # Test user registration with admin credentials
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.test_user_data["username"])

        # Attempt to register the same user again, expecting failure
        response = self.client.post(self.register_url, self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_registration_with_non_admin_user(self):
        # Create a non-admin user
        non_admin_user_data = {
            "username": "nonadminuser",
            "password": "nonadminpassword",
        }
        non_admin_user = User.objects.create_user(**non_admin_user_data)

        # Obtain JWT token for the non-admin user
        response = self.client.post(self.login_url, non_admin_user_data)
        non_admin_token = response.data["access"]

        # Set the non-admin token in the request headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {non_admin_token}")

        # Attempt to register a new user with non-admin credentials
        response = self.client.post(self.register_url, self.test_user_data)

        # Expecting 403 Forbidden because non-admins cannot register users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserLoginTests(APITestCase):
    def setUp(self):
        # URL path for login
        self.login_url = reverse("login")

        # Create a test user
        self.test_user_data = {"username": "testuser", "password": "testpassword123"}
        self.user = User.objects.create_user(**self.test_user_data)

    def test_user_login_with_valid_credentials(self):
        # Attempt login with valid credentials
        response = self.client.post(self.login_url, self.test_user_data)

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure both access and refresh tokens are returned
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_with_invalid_credentials(self):
        # Attempt login with incorrect password
        invalid_credentials = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, invalid_credentials)

        # Check if the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that an error message is returned
        self.assertIn("error", response.data)

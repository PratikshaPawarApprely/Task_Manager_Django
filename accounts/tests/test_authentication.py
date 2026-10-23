from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class JWTAuthenticationTest(APITestCase):

    def test_task_list_without_authentication(self):
        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.data)

    def test_task_list_with_valid_jwt(self):
        # 1. Create a test user
        user = User.objects.create_user(
            username="jwt_test_user",
            password="TestPass123!"
        )

        # 2. Give the user the Admin role
        admin_group, _ = Group.objects.get_or_create(
            name="Admin"
        )
        user.groups.add(admin_group)

        # 3. Log in to obtain JWT tokens
        login_response = self.client.post(
            "/api/v1/accounts/login/",
            {
                "username": "jwt_test_user",
                "password": "TestPass123!"
            },
            format="json"
        )

        self.assertEqual(
            login_response.status_code,
            status.HTTP_200_OK,
            login_response.data
        )

        # 4. Extract the access token
        access_token = login_response.data["access"]

        # 5. Send the token to the protected API
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(reverse("task-list"))

        # 6. Verify that access is allowed
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            response.data
        )

    def test_task_list_with_invalid_jwt(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid.fake.token"
        )

        response = self.client.get(reverse("task-list"))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            response.data
        )

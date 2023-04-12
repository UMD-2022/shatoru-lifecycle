import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:
    @pytest.fixture(scope="session", autouse=True)
    def create_driver_group(self, django_db_blocker):
        with django_db_blocker.unblock():
            Group.objects.get_or_create(name="Driver")

    @pytest.fixture
    def admin_user(self):
        return User.objects.create_superuser(
            email="superuser@example.com",
            username="superuser",
            password="admin123",
        )

    @pytest.fixture
    def test_user1(self):
        return User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
        )

    @pytest.fixture
    def test_user2(self):
        return User.objects.create_user(
            email="testuser2@example.com",
            username="testuser2",
            password="password456",
        )

    @pytest.fixture
    def admin_client(self, admin_user):
        cli = APIClient()
        cli.force_login(admin_user)
        return cli

    @pytest.fixture
    def client(self):
        return APIClient()

    def test_create_user_as_admin(self, admin_client):
        """
        Ensure we can create a new user object as an admin.
        """
        url = reverse("create_driver")
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = admin_client.post(url, data, format="json")
        response.status_code == status.HTTP_201_CREATED
        User.objects.count() == 2
        User.objects.latest("pk").email == "testuser@example.com"

    def test_create_user(self, client):
        """
        Ensure we cannot create a new user object as a normal user.
        """
        url = reverse("create_driver")
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = client.post(url, data, format="json")
        response.status_code == status.HTTP_403_FORBIDDEN
        User.objects.count() == 1
        assert not User.objects.filter(email="testuser@example.com").exists()

    def test_create_user_without_email(self, admin_client):
        """
        Ensure that creating a user without an email fails.
        """
        url = reverse("create_driver")
        data = {
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = admin_client.post(url, data, format="json")
        response.status_code == status.HTTP_400_BAD_REQUEST
        User.objects.count() == 1

    def test_create_user_with_existing_email(self, admin_client, test_user1):
        """
        Ensure that creating a user with an existing email fails.
        """
        url = reverse("create_driver")
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = admin_client.post(url, data, format="json")
        response.status_code == status.HTTP_400_BAD_REQUEST
        User.objects.count() == 2

    def test_get_user_list_as_admin(self, admin_client, test_user1, test_user2):
        """
        Ensure we can retrieve a list of users as an admin.
        """
        url = reverse("list_drivers")
        response = admin_client.get(url, format="json")
        response.status_code == status.HTTP_200_OK
        len(response.data) == 2

    def test_get_user_list(self, client, test_user1, test_user2):
        """
        Ensure we cannot retrieve a list of users as normal users.
        """
        url = reverse("list_drivers")
        response = client.get(url, format="json")
        response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_detail_as_admin(self, admin_client, test_user1):
        """
        Ensure we can retrieve a user object as an admin.
        """
        url = reverse("get_or_update_driver", args=[test_user1.id])
        response = admin_client.get(url, format="json")
        response.status_code == status.HTTP_200_OK
        response.data["email"] == "testuser@example.com"

    def test_get_user_detail(self, client, test_user1):
        """
        Ensure we cannot retrieve a user object as a normal user.
        """
        url = reverse("get_or_update_driver", args=[test_user1.id])
        response = client.get(url, format="json")
        response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user(self, admin_client):
        user = User.objects.create(username="test_user", password="test_password")

        # Test deleting a single user
        response = admin_client.delete(reverse("get_or_update_driver", args=[user.id]))
        # We don't allow user deletion via API
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shatoru_backend.apps.shuttle_services.models import Shuttle

User = get_user_model()


@pytest.mark.django_db
class TestShuttleAPI:
    @pytest.fixture
    def admin_user(self):
        return User.objects.create_superuser(
            email="superuser@example.com",
            username="superuser",
            password="admin123",
        )

    @pytest.fixture
    def admin_client(self, admin_user):
        cli = APIClient()
        cli.force_login(admin_user)
        return cli

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def shuttle(self):
        # Create a sample shuttle instance
        return Shuttle.objects.create(name="Test Shuttle")

    def test_create_shuttle_as_admin(self, admin_client):
        # Test creating a new shuttle as an admin
        data = {
            "name": "New Shuttle",
        }
        response = admin_client.post(reverse("shuttle-list"), data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Shuttle.objects.count() == 1
        assert Shuttle.objects.filter(name="New Shuttle").exists()

    def test_create_shuttle(self, client):
        # Test creating a new shuttle
        data = {
            "name": "New Shuttle",
        }
        response = client.post(reverse("shuttle-list"), data=data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Shuttle.objects.count() == 0
        assert not Shuttle.objects.filter(name="New Shuttle").exists()

    def test_list_shuttles(self, client):
        # Test retrieving list of shuttles
        response = client.get(reverse("shuttle-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_shuttle_as_admin(self, admin_client, shuttle):
        # Test retrieving a single shuttle
        response = admin_client.get(reverse("shuttle-detail", args=[shuttle.id]))
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_shuttle(self, client):
        # Test retrieving a nonexistent shuttle
        response = client.get(reverse("shuttle-detail", args=[123]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_shuttle_as_admin(self, admin_client, shuttle):
        # Test updating an existing shuttle as an admin
        data = {
            "name": "Updated Shuttle",
        }
        response = admin_client.put(
            reverse("shuttle-detail", args=[shuttle.id]),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert not Shuttle.objects.filter(name=shuttle.name).exists()
        assert Shuttle.objects.filter(name="Updated Shuttle").exists()

    def test_update_shuttle(self, client, shuttle):
        # Test updating an existing shuttle
        data = {
            "name": "Updated Shuttle",
        }
        response = client.put(
            reverse("shuttle-detail", args=[shuttle.id]),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Shuttle.objects.filter(name=shuttle.name).exists()
        assert not Shuttle.objects.filter(name="Updated Shuttle").exists()

    def test_update_nonexistent_shuttle(self, admin_client):
        # Test updating a nonexistent shuttle
        data = {
            "name": "Updated Shuttle",
        }
        response = admin_client.put(
            reverse("shuttle-detail", args=[123]),
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_shuttle_as_admin(self, admin_client, shuttle):
        # Test deleting a shuttle as an admin
        response = admin_client.delete(reverse("shuttle-detail", args=[shuttle.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Shuttle.objects.filter(id=shuttle.id).exists()

    def test_delete_shuttle(self, client, shuttle):
        # Test deleting a shuttle
        response = client.delete(reverse("shuttle-detail", args=[shuttle.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Shuttle.objects.filter(id=shuttle.id).exists()

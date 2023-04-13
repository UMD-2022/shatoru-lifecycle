import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shatoru_backend.apps.routing.models import Stop

User = get_user_model()


@pytest.mark.django_db
class TestStopAPI:
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
    def stop1(self):
        # Create a sample shuttle instance
        return Stop.objects.create(name="Stop 1", abbr="S1")

    @pytest.fixture
    def stop2(self):
        # Create a sample shuttle instance
        return Stop.objects.create(name="Stop 2", abbr="S2")

    def test_create_stop_as_admin(self, admin_client):
        url = reverse("stop-list")
        data = {
            "name": "Stop 1",
            "abbr": "S1",
        }
        response = admin_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Stop.objects.filter(abbr="S1").exists()

    def test_create_stop(self, client):
        url = reverse("stop-list")
        data = {
            "name": "Stop 1",
            "abbr": "S1",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Stop.objects.filter(abbr="S1").exists()

    def test_create_stop_without_required_fields(self, admin_client):
        url = reverse("stop-list")
        data = {"name": "Stop1"}
        response = admin_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_stops(self, client, stop1, stop2):
        url = reverse("stop-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_stop(self, client, stop1):
        url = reverse("stop-detail", kwargs={"pk": stop1.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["abbr"] == stop1.abbr

    def test_retrieve_nonexistent_stop(self, client):
        url = reverse("stop-detail", kwargs={"pk": 123})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_stop_as_admin(self, admin_client, stop1):
        url = reverse("stop-detail", kwargs={"pk": stop1.id})
        data = {"name": "Updated Stop 1", "abbr": "US1"}
        response = admin_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert not Stop.objects.filter(abbr=stop1.abbr).exists()
        assert Stop.objects.filter(abbr="US1").exists()

    def test_update_stop(self, client, stop1):
        url = reverse("stop-detail", kwargs={"pk": stop1.id})
        data = {"name": "Updated Stop 1", "abbr": "US1"}
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Stop.objects.filter(abbr=stop1.abbr).exists()
        assert not Stop.objects.filter(abbr="US1").exists()

    def test_update_nonexistent_stop(self, admin_client):
        url = reverse("stop-detail", kwargs={"pk": 123})
        data = {"name": "Updated Stop1", "abbr": "US1"}
        response = admin_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_stop_as_admin(self, admin_client, stop1):
        url = reverse("stop-detail", kwargs={"pk": stop1.id})
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Stop.objects.filter(abbr=stop1.abbr).exists()

    def test_delete_stop(self, client, stop1):
        url = reverse("stop-detail", kwargs={"pk": stop1.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Stop.objects.filter(abbr=stop1.abbr).exists()

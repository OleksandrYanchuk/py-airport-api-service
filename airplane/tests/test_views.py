from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from airplane.models import AirplaneType
from airplane.views import AirplaneTypeViewSet, AirplaneViewSet


class AirplaneTypeViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AirplaneTypeViewSet.as_view(
            {"get": "list", "post": "create"}
        )  # Додано дозвіл POST-запитів
        self.uri = reverse("airplane:airplanetype-list")  # Виправлено reverse
        self.admin_user = get_user_model().objects.create_user(
            "admin@user.com", "password", is_staff=True
        )

        self.airplane_type_data = {"name": "Boeing 747"}

    def test_list_airplane_types(self):
        # Перевірте, чи можна отримати список типів літаків
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_airplane_type(self):
        # Перевірте, чи можна створити новий тип літака
        request = self.factory.post(self.uri, self.airplane_type_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_airplane_type_unauthorized(self):
        # Перевірте, чи безавторизований користувач не може створити новий тип літака
        request = self.factory.post(self.uri, self.airplane_type_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AirplaneViewSetTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AirplaneViewSet.as_view(
            {"get": "list", "post": "create"}
        )  # Додано дозвіл POST-запитів
        self.uri = reverse("airplane:airplane-list")  # Виправлено reverse
        self.admin_user = get_user_model().objects.create_user(
            "admin@user.com", "password", is_staff=True
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")

        self.airplane_data = {
            "name": "Airplane1",
            "rows": 10,
            "seats_in_row": 6,
            "airplane_type": self.airplane_type.id,
        }

    def test_list_airplanes(self):
        # Перевірте, чи можна отримати список літаків
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_airplane(self):
        # Перевірте, чи можна створити новий літак
        request = self.factory.post(self.uri, self.airplane_data)
        force_authenticate(request, user=self.admin_user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_airplane_unauthorized(self):
        # Перевірте, чи безавторизований користувач не може створити новий літак
        request = self.factory.post(self.uri, self.airplane_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

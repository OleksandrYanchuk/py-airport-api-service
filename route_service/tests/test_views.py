from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from route_service.views import AirportViewSet, RouteViewSet
from route_service.models import Airport, Route
from route_service.serializers import AirportSerializer, RouteSerializer


class AirportViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AirportViewSet.as_view({'get': 'list', 'post': 'create', 'retrieve': 'retrieve'})
        self.user = get_user_model().objects.create_user("admin@user.com", "password", is_staff=True)
        self.airport_data = {
            "icao": "Test",
            "iata": "Test",
            "name": "Test Airport",
            "city": "Test_city",
            "state": "TC",
            "country": "USA",
            "elevation": 13,
            "lat": "45.6413",
            "lon": "-73.7781",
            "tz": "America/New_York",
            "lid": "US"
        }
        self.airport = Airport.objects.create(**self.airport_data)

    def test_list_airports(self):
        request = self.factory.get('/airports/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        # Extract the data from the paginated response
        data = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, serializer.data)

    def test_create_airport(self):
        request = self.factory.post('/airports/', data=self.airport_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 2)

    def test_create_airport_unauthorized(self):
        request = self.factory.post('/airports/', data=self.airport_data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Airport.objects.count(), 1)

    def test_retrieve_airport_unauthorized(self):
        request = self.factory.get(f'/airports/{self.airport.pk}/')
        response = self.view(request, pk=self.airport.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_non_existent_airport(self):
        client = APIClient()
        non_existent_pk = self.airport.pk + 1
        response = client.get(f'/airports/{non_existent_pk}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RouteViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RouteViewSet.as_view({'get': 'list', 'post': 'create'})
        self.user = get_user_model().objects.create_user("admin@user.com", "password", is_staff=True)
        self.source_airport = Airport.objects.create(icao="KJFK", iata="JFK", name="John F. Kennedy International Airport",
                                                     city="New York", state="NY", country="USA", elevation=13,
                                                     lat="40.6413", lon="-73.7781", tz="America/New_York", lid="US")
        self.destination_airport = Airport.objects.create(icao="EGLL", iata="LHR", name="Heathrow Airport",
                                                          city="London", state="London", country="UK", elevation=83,
                                                          lat="51.4700", lon="-0.4543", tz="Europe/London", lid="GB")


    def test_create_route(self):
        data = {
            "source": self.source_airport.pk,
            "destination": self.destination_airport.pk,
            "distance": 5568
        }
        request = self.factory.post('/routes/', data=data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 1)

    def test_create_route_unauthorized(self):
        data = {
            "source": self.source_airport.pk,
            "destination": self.destination_airport.pk,
            "distance": 5568
        }
        request = self.factory.post('/routes/', data=data)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Route.objects.count(), 0)

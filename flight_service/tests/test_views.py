from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from airplane.models import Airplane, AirplaneType
from route_service.models import Airport, Route
from ..models import Crew, Flight
from ..serializers import CrewSerializer, FlightSerializer
from ..views import CrewViewSet, FlightViewSet


class CrewViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CrewViewSet.as_view(
            {"get": "list", "post": "create", "retrieve": "retrieve"}
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.user = get_user_model().objects.create_user(
            "admin@user.com", "password", is_staff=True
        )

    def test_get_crew_list(self):
        request = self.factory.get("/crews/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, serializer.data)

    def test_create_crew(self):
        data = {"first_name": "Jane", "last_name": "Smith"}
        request = self.factory.post("/crews/", data=data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 2)


class FlightViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FlightViewSet.as_view(
            {"get": "list", "post": "create", "retrieve": "retrieve"}
        )
        self.user = get_user_model().objects.create_user(
            "admin@user.com", "password", is_staff=True
        )
        self.source_airport = Airport.objects.create(
            icao="KJFK",
            iata="JFK",
            name="John F. Kennedy International Airport",
            city="New York",
            state="NY",
            country="USA",
            elevation=13,
            lat="40.6413",
            lon="-73.7781",
            tz="America/New_York",
            lid="US",
        )
        self.destination_airport = Airport.objects.create(
            icao="EGLL",
            iata="LHR",
            name="Heathrow Airport",
            city="London",
            state="London",
            country="UK",
            elevation=83,
            lat="51.4700",
            lon="-0.4543",
            tz="Europe/London",
            lid="GB",
        )
        self.airplane_type = AirplaneType.objects.create(name="boeing")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=5,
            seats_in_row=4,
            airplane_type=self.airplane_type,
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
        )
        self.flight = Flight.objects.create(
            airplane=self.airplane,
            departure_time=datetime(2023, 7, 20, 12, 0),
            arrival_time=datetime(2023, 7, 20, 15, 0),
        )
        self.flight.route.add(self.route)

    def test_get_flight_list(self):
        request = self.factory.get("/flights/")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        flights = Flight.objects.all()
        serializer = FlightSerializer(flights, many=True)
        data = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, serializer.data)

from django.test import TestCase

from route_service.models import Airport, Route
from route_service.serializers import AirportSerializer, RouteSerializer


class AirportSerializerTest(TestCase):
    def setUp(self):
        self.airport_data = {
            "icao": "KJFK",
            "iata": "JFK",
            "name": "John F. Kennedy International Airport",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "elevation": 13,
            "lat": "40.6413",
            "lon": "-73.7781",
            "tz": "America/New_York",
            "lid": "US",
        }
        self.airport = Airport.objects.create(**self.airport_data)
        self.serializer = AirportSerializer(instance=self.airport)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()), set(["id", "name", "city", "state", "country"])
        )


class RouteSerializerTest(TestCase):
    def setUp(self):
        self.source_airport = Airport.objects.create(
            name="Source Airport",
            city="City1",
            state="State1",
            country="Country1",
            lat="40.6413",
            lon="-73.7781",
        )
        self.dest_airport = Airport.objects.create(
            name="Destination Airport",
            city="City2",
            state="State2",
            country="Country2",
            lat="41.6413",
            lon="-74.7781",
        )
        self.route_data = {
            "source": self.source_airport,
            "destination": self.dest_airport,
            "distance": 123.45,
        }
        self.route = Route.objects.create(**self.route_data)
        self.serializer = RouteSerializer(instance=self.route)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()), set(["id", "source", "destination", "distance"])
        )

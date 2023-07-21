from django.test import TestCase


class CrewSerializerTest(TestCase):
    def test_crew_serializer(self):
        crew = Crew.objects.create(first_name="John", last_name="Doe")
        serializer = CrewSerializer(crew)
        expected_data = {
            "id": crew.id,
            "first_name": "John",
            "last_name": "Doe",
        }
        self.assertEqual(serializer.data, expected_data)


from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from airplane.models import Airplane, AirplaneType
from route_service.models import Route, Airport
from flight_service.models import Crew, Flight
from flight_service.serializers import (
    CrewSerializer,
    TicketSerializer,
)


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=5,
            seats_in_row=4,
            airplane_type=self.airplane_type,
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
        self.dest_airport = Airport.objects.create(
            icao="EGLL",
            iata="LHR",
            name="Heathrow Airport",
            city="London",
            state="England",
            country="UK",
            elevation=25,
            lat="51.4700",
            lon="-0.4543",
            tz="Europe/London",
            lid="GB",
        )
        self.route = Route.objects.create(
            source=self.source_airport, destination=self.dest_airport
        )
        self.flight = Flight.objects.create(
            airplane=self.airplane,
            departure_time=timezone.now(),
            arrival_time=timezone.now() + timedelta(hours=3),
        )
        self.flight.route.add(self.route)
        self.ticket_data = {
            "row": 1,
            "seat": 1,
            "flight": self.flight.id,
        }

    def test_ticket_serializer_with_valid_data(self):
        serializer = TicketSerializer(data=self.ticket_data)
        self.assertTrue(serializer.is_valid())

    def test_ticket_serializer_with_invalid_data(self):
        self.ticket_data["row"] = 10
        serializer = TicketSerializer(data=self.ticket_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("row", serializer.errors)

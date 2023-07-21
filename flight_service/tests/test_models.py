import time

from _decimal import Decimal
from django.contrib.auth import get_user_model

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from airplane.models import Airplane, AirplaneType
from route_service.models import Route, Airport
from flight_service.models import Crew, Flight, Order, Ticket

class CrewModelTest(TestCase):
    def test_crew_str_representation(self):
        crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(str(crew), "John Doe")


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("admin@user.com", "password", is_staff=True)
        self.order = Order.objects.create(user=self.user)

    def test_order_str_representation(self):
        self.assertEqual(str(self.order), str(self.order.created_at))


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("admin@user.com", "password", is_staff=True)
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane = Airplane.objects.create(name="Test Airplane", rows=5, seats_in_row=4,
                                                airplane_type=self.airplane_type)
        self.source_airport = Airport.objects.create(
            icao='KJFK',
            iata='JFK',
            name='John F. Kennedy International Airport',
            city='New York',
            state='NY',
            country='USA',
            elevation=13,
            lat=Decimal('40.6413'),
            lon=Decimal('-73.7781'),
            tz='America/New_York',
            lid='US'
        )
        self.dest_airport = Airport.objects.create(
            icao='EGLL',
            iata='LHR',
            name='Heathrow Airport',
            city='London',
            state='England',
            country='UK',
            elevation=25,
            lat=Decimal('51.4700'),
            lon=Decimal('-0.4543'),
            tz='Europe/London',
            lid='GB'
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.dest_airport,
        )
        self.flight = Flight.objects.create(
            airplane=self.airplane,
            departure_time=timezone.now(),
            arrival_time=timezone.now(),
        )
        self.flight.route.add(self.route)
        self.order = Order.objects.create(user=self.user)

    def test_ticket_validation_valid_values(self):
        # Test valid row and seat numbers
        row = 1
        seat = 1
        try:
            Ticket.validate_ticket(row, seat, self.airplane, ValidationError)
        except ValidationError:
            self.fail("validate_ticket() raised a ValidationError unexpectedly.")

    def test_ticket_validation_invalid_values(self):
        # Test invalid row and seat numbers
        row = 10
        seat = 5
        with self.assertRaises(ValidationError):
            Ticket.validate_ticket(row, seat, self.airplane, ValidationError)
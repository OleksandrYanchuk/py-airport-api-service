from django.test import TestCase
from decimal import Decimal
from geopy.distance import geodesic
from route_service.models import Airport, Route


class AirportModelTest(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(
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

    def test_airport_str_representation(self):
        self.assertEqual(str(self.airport), 'John F. Kennedy International Airport')


class RouteModelTest(TestCase):
    def setUp(self):
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

    def test_route_str_representation(self):
        self.assertEqual(str(self.route), 'John F. Kennedy International Airport to Heathrow Airport')

    def test_calculate_distance_signal(self):
        source_coords = (self.source_airport.lat, self.source_airport.lon)
        dest_coords = (self.dest_airport.lat, self.dest_airport.lon)
        expected_distance = geodesic(source_coords, dest_coords).kilometers

        route = Route.objects.create(
            source=self.source_airport,
            destination=self.dest_airport,
        )

        self.assertEqual(route.distance, expected_distance)

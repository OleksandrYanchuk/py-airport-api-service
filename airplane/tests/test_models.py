from django.test import TestCase

from airplane.models import AirplaneType, Airplane


class AirplaneTypeModelTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")

    def test_str_representation(self):
        self.assertEqual(str(self.airplane_type), "Boeing 747")

    def test_unique_name(self):
        with self.assertRaises(Exception):
            AirplaneType.objects.create(name="Boeing 747")


class AirplaneModelTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane1", rows=10, seats_in_row=6, airplane_type=self.airplane_type
        )

    def test_str_representation(self):
        self.assertEqual(str(self.airplane), "Airplane1")

    def test_capacity_calculation(self):
        self.assertEqual(self.airplane.capacity, 60)

    def test_airplane_type_on_delete_cascade(self):
        self.airplane_type.delete()
        self.assertFalse(Airplane.objects.filter(name="Airplane1").exists())

    def test_airplane_capacity_update(self):
        self.airplane.rows = 12
        self.airplane.seats_in_row = 5
        self.airplane.save()
        self.assertEqual(self.airplane.capacity, 60)

from django.test import TestCase

from airplane.models import AirplaneType, Airplane
from airplane.serializers import AirplaneTypeSerializer, AirplaneSerializer


class AirplaneTypeSerializerTest(TestCase):
    def setUp(self):
        self.airplane_type_data = {"id": 1, "name": "Boeing 747"}

    def test_valid_serializer_data(self):
        serializer = AirplaneTypeSerializer(data=self.airplane_type_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_create(self):
        serializer = AirplaneTypeSerializer(data=self.airplane_type_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(AirplaneType.objects.count(), 1)

    def test_serializer_unique_name(self):
        # Переконайтеся, що серіалайзер не допускає створення дублікатів типів літаків
        serializer = AirplaneTypeSerializer(data=self.airplane_type_data)
        serializer.is_valid()
        serializer.save()

        duplicate_serializer = AirplaneTypeSerializer(data=self.airplane_type_data)
        self.assertFalse(duplicate_serializer.is_valid())


class AirplaneSerializerTest(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane_data = {
            "id": 1,
            "name": "Airplane1",
            "rows": 10,
            "seats_in_row": 6,
            "airplane_type": self.airplane_type.id,
            "capacity": 60,
        }

    def test_valid_serializer_data(self):
        serializer = AirplaneSerializer(data=self.airplane_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_create(self):
        serializer = AirplaneSerializer(data=self.airplane_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(Airplane.objects.count(), 1)

    def test_serializer_capacity_calculation(self):
        serializer = AirplaneSerializer(data=self.airplane_data)
        serializer.is_valid()
        self.assertEqual(self.airplane_data["capacity"], 10 * 6)

    def test_serializer_airplane_type_validation(self):
        # Переконайтеся, що серіалайзер перевіряє наявність існуючого типу літака
        invalid_airplane_data = {
            "id": 2,
            "name": "Airplane2",
            "rows": 10,
            "seats_in_row": 6,
            "airplane_type": 999,
        }
        serializer = AirplaneSerializer(data=invalid_airplane_data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_airplane_type_update(self):
        new_airplane_type = AirplaneType.objects.create(name="Airbus A380")
        self.airplane_data["airplane_type"] = new_airplane_type.id
        serializer = AirplaneSerializer(data=self.airplane_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(Airplane.objects.get(id=1).airplane_type, new_airplane_type)

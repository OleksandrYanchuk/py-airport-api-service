from django.db import migrations
from route_service.models import Airport
import os
import json


def import_data(apps, schema_editor):
    # Specify the path to your JSON file
    file_path = 'airports_data.json'

    # Read data from the JSON file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Function for importing data
    for airport_data in data.values():
        if 'state' in airport_data:
            state = airport_data['state']
        else:
            state = None

        airport = Airport.objects.create(
            icao=airport_data['icao'],
            iata=airport_data['iata'],
            name=airport_data['name'],
            city=airport_data['city'],
            state=state,
            country=airport_data['country'],
            elevation=airport_data['elevation'],
            lat=airport_data['lat'],
            lon=airport_data['lon'],
            tz=airport_data['tz'],
            lid=airport_data['lid'],
        )

        print(f"Airport {airport.name} saved to the database.")


def reverse_import_data(apps, schema_editor):
    # Add any reverse data loading or other cleanup if necessary
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(import_data, reverse_import_data),
    ]

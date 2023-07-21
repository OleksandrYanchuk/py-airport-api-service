import os
import django
import json
from concurrent.futures import ThreadPoolExecutor

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_api_service.settings')

# Initialize Django
django.setup()

# Now you can import Django models and perform other Django-related actions
from route_service.models import Airport

# Specify the path to your JSON file
file_path = 'airports_data.json'

# Read data from the JSON file
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# Function for importing data
def import_data(airport_data):
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

# Number of threads to use for parallel execution
num_threads = 4

# Use ThreadPoolExecutor to run the import_data function in parallel
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    executor.map(import_data, data.values())

print("Data import completed.")

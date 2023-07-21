from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.distance import geodesic


class Airport(models.Model):
    icao = models.TextField(blank=True, null=True)
    iata = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    lon = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    tz = models.TextField(blank=True, null=True)
    lid = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.source.name} to {self.destination.name}"


@receiver(pre_save, sender=Route)
def calculate_distance(sender, instance, **kwargs):
    source_coords = (instance.source.lat, instance.source.lon)
    dest_coords = (instance.destination.lat, instance.destination.lon)
    instance.distance = geodesic(source_coords, dest_coords).kilometers

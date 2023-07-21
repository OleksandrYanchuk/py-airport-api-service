# Generated by Django 4.0.4 on 2023-07-21 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("flight_service", "0001_initial"),
        ("airplane", "0001_initial"),
        ("route_service", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="airplane",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="airplane.airplane"
            ),
        ),
        migrations.AddField(
            model_name="flight",
            name="crew",
            field=models.ManyToManyField(blank=True, to="flight_service.crew"),
        ),
        migrations.AddField(
            model_name="flight",
            name="route",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="route_service.route"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("flight", "row", "seat")},
        ),
    ]

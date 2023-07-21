# Generated by Django 4.0.4 on 2023-07-21 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route_service', '0001_initial'),
        ('flight_service', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='route',
        ),
        migrations.AddField(
            model_name='flight',
            name='route',
            field=models.ManyToManyField(to='route_service.route'),
        ),
    ]
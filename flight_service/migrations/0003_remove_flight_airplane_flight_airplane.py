# Generated by Django 4.0.4 on 2023-07-19 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airplane', '0001_initial'),
        ('flight_service', '0002_alter_crew_first_name_alter_crew_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='airplane',
        ),
        migrations.AddField(
            model_name='flight',
            name='airplane',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='airplane.airplane'),
            preserve_default=False,
        ),
    ]
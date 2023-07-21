from django.core.management import call_command
from django.db import migrations


def func(apps, schema_editor):
    call_command("loaddata", "data.json")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_auto"),
    ]

    operations = [
        migrations.RunPython(func, reverse_func),
    ]

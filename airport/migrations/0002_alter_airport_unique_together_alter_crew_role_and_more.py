# Generated by Django 5.1.4 on 2024-12-30 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="airport",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="crew",
            name="role",
            field=models.CharField(
                choices=[
                    ("PILOT", "Pilot"),
                    ("CO-PILOT", "Co-pilot"),
                    ("FLIGHT ATTENDANT", "Flight attendant"),
                ],
                max_length=63,
            ),
        ),
        migrations.AddConstraint(
            model_name="airport",
            constraint=models.UniqueConstraint(
                fields=("name", "closest_big_city"),
                name="Unique name of the city and airport",
            ),
        ),
    ]

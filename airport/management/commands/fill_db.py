from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from airport.services.db_population import (
    add_airports,
    add_routes,
    add_crews,
    add_users,
    add_orders,
    add_airplanes,
    add_flights,
    add_tickets
)


class Command(BaseCommand):
    help = "Populate the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "user_input",
            nargs="?",
            type=int,
            default=30,
            help="Number of entries to create (default: 30)"
        )

    def handle(self, *args, **kwargs):
        user_input = kwargs.get("user_input")

        services = [
            add_airports.add_airports,
            add_crews.add_crews,
            add_routes.add_routes,
            add_orders.add_orders,
            add_airplanes.add_airplanes,
            add_flights.add_flight,
            add_tickets.add_tickets
        ]

        try:
            add_users.add_users()

            for service in services:
                service(user_input=user_input)

        except ValidationError as e:
            print(f"Validation error: {e}")
        except IntegrityError as e:
            print(f"Database integrity error: {e}")
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        else:
            print("The database was filled successfully")

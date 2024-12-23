from django.core.management.base import BaseCommand

from airport.services.db_population import (
    add_airports,
    add_routes,
    add_crews,
    add_users,
    add_orders,
    add_airplanes,
    add_flight
)


class Command(BaseCommand):
    help_ = "Populate the database"

    def handle(self, *args, **kwargs):
        # add_users.add_users()
        # add_airports.add_airports()
        # add_crews.add_crews()
        # add_routes.add_routes()
        # add_orders.add_orders()
        # add_airplanes.add_airplanes()
        add_flight.add_flight()

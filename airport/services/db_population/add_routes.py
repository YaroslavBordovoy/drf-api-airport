import random

from airport.models import Route, Airport
from airport.services.utils.distance_calcultion import (
    get_coord,
    calculate_distance,
)


def add_routes(user_input: int):
    cities = list(Airport.objects.values_list("closest_big_city", flat=True))
    routes = []

    for _ in range(user_input):
        source_city = random.choice(cities)
        destination_city = random.choice(cities)

        while source_city == destination_city:
            destination_city = random.choice(cities)

        try:
            source_coords = get_coord(city=source_city)
            destination_coords = get_coord(city=destination_city)

            distance = calculate_distance(source_coords, destination_coords)

            source_airport = Airport.objects.filter(
                closest_big_city=source_city
            ).first()
            destination_airport = Airport.objects.filter(
                closest_big_city=destination_city
            ).first()

            routes.append(
                Route(
                    source=source_airport,
                    destination=destination_airport,
                    distance=distance
                )
            )
        except ValueError:
            print("There is no data for the city you specified.")
            continue

    Route.objects.bulk_create(routes)

    print(f"Routes added successfully: {user_input}")

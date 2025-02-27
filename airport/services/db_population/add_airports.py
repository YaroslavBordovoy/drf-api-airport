import csv
import os
import random

from airport.models import Airport


DATA_CITIES_LITE_PATH = os.environ.get("DATA_CITIES_LITE_PATH")


def get_cities(user_input: int) -> list[str]:
    cities = []

    if not DATA_CITIES_LITE_PATH:
        raise FileNotFoundError("The required file was not found.")

    with open(DATA_CITIES_LITE_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["population"] and float(row["population"]) > 100_000:
                cities.append(row["city_ascii"])

    random.shuffle(cities)

    return cities[:user_input]


def create_airports(cities: list[str]) -> list[dict]:
    airports = []
    suffixes = (
        "International Airport",
        "Regional Airport",
        "Airfield",
        "Aerodrome"
    )

    for city in cities:
        airport = f"{city} {random.choice(suffixes)}"

        airports.append({"name": airport, "closest_big_city": city})

    return airports


def add_airports(user_input: int) -> None:
    cities = get_cities(user_input)
    airports = create_airports(cities)

    existing_airports = set(
        Airport.objects.values_list("name", "closest_big_city")
    )
    unique_airports = [
        airport for airport in airports
        if (airport["name"],
            airport["closest_big_city"]) not in existing_airports
    ]

    airport_objects = [Airport(**airport) for airport in unique_airports]
    Airport.objects.bulk_create(airport_objects)

    print(f"Airports added successfully: {user_input}")

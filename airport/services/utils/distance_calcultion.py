import csv
import math
import os


DATA_CITIES_PATH = os.environ.get("DATA_CITIES_PATH")

city_cache = {}


def get_coord(city: str) -> dict:
    if city in city_cache:
        return city_cache.get(city)

    if not DATA_CITIES_PATH:
        raise FileNotFoundError("The required file was not found.")

    with open(DATA_CITIES_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["city_ascii"] == city:
                city_coords = {
                    "lat": float(row["lat"]),
                    "lng": float(row["lng"]),
                }
                city_cache[city] = city_coords

                return city_coords

    raise ValueError("There is no data for the city you specified.")


def calculate_distance(source_coords: dict, destination_coords: dict) -> float:
    lat_1, lng_1 = source_coords["lat"], source_coords["lng"]
    lat_2, lng_2 = destination_coords["lat"], destination_coords["lng"]
    earth_radius = 6371

    lat_1, lng_1, lat_2, lng_2 = map(
        math.radians, [lat_1, lng_1, lat_2, lng_2]
    )

    delta_lat = lat_2 - lat_1
    delta_lng = lng_2 - lng_1

    intermediate_distance = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat_1) * math.cos(lat_2) * math.sin(delta_lng / 2) ** 2
    )
    central_angle = 2 * math.atan2(
        math.sqrt(intermediate_distance), math.sqrt(1 - intermediate_distance)
    )

    return earth_radius * central_angle

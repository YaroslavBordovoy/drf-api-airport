import csv
import os


DATA_CITIES_PATH = os.environ.get("DATA_CITIES_PATH")


def get_city(city) -> bool:
    if not DATA_CITIES_PATH:
        raise FileNotFoundError("The required file was not found.")

    with open(DATA_CITIES_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["city_ascii"].lower() == city.lower():
                return True

    return False

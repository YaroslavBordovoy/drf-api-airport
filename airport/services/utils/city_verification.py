import csv


FILE_PATH = "airport/services/data/data_cities_lite.csv"


def get_city(city) -> bool:
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["city_ascii"].lower() == city.lower():
                return True

    return False

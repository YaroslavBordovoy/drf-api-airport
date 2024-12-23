import random

from airport.choices import AirplaneName
from airport.models import Airplane, AirplaneType


def add_airplanes(user_input: int = 10) -> None:
    airplane_objects = []

    for _ in range(user_input):
        airplane = Airplane(
            name=random.choice([choice[0] for choice in AirplaneName.choices]),
            rows=random.randint(15, 40),
            seats_in_row=random.randint(4, 6),
        )

        airplane_type_name = airplane.type_of_plane()
        airplane.airplane_type, _ = AirplaneType.objects.get_or_create(
            name=airplane_type_name
        )

        airplane_objects.append(airplane)

    Airplane.objects.bulk_create(airplane_objects)

    print("Airplanes added successfully")

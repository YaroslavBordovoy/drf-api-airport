import random
from datetime import datetime, timedelta

from airport.models import Flight, Route, Airplane, Crew


def get_time() -> tuple:
    start_date = datetime.now() + timedelta(days=5)
    end_date = start_date + timedelta(days=120)

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    time_span_min = 1800
    time_span_max = 43200

    departure_time = datetime.fromtimestamp(
        random.randint(start_timestamp, end_timestamp)
    )
    arrival_time = departure_time + timedelta(
        seconds=random.randint(time_span_min, time_span_max)
    )

    return departure_time, arrival_time


def add_flight(user_input: int) -> None:
    routes = Route.objects.all()
    airplanes = Airplane.objects.all()
    crews = Crew.objects.all()

    pilots = crews.filter(role="P")
    co_pilots = crews.filter(role="CP")
    flight_attendants = crews.filter(role="FA")

    flight_objects = []

    for _ in range(user_input):
        departure_time, arrival_time = get_time()

        flight = Flight(
            route=random.choice(routes),
            airplane=random.choice(airplanes),
            departure_time=departure_time,
            arrival_time=arrival_time,
        )
        flight.save()
        flight_objects.append(flight)

    for flight in flight_objects:
        pilot = random.choice(pilots)
        co_pilot = random.choice(co_pilots)
        flight_attendant = [
            random.choice(flight_attendants)
            for _ in range(random.randint(1, 3))
        ]

        crew_members = [pilot, co_pilot] + flight_attendant

        flight.crew.add(*crew_members)

    print(f"Flights added successfully: {user_input}")

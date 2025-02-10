import random

from airport.models import Ticket, Order, Flight


def add_tickets(user_input: int) -> None:
    orders = Order.objects.all()
    flights = Flight.objects.all()

    ticket_objects = []

    for _ in range(user_input):
        current_flights = random.choice(flights)
        airplane = current_flights.airplane

        rows = airplane.rows
        seats_in_row = airplane.seats_in_row

        taken_seats = set(
            Ticket.objects.filter(
                flight=current_flights
            ).values_list("row", "seat")
        )

        row = random.randint(1, rows)
        seat = random.randint(1, seats_in_row)

        while (row, seat) in taken_seats:
            row = random.randint(1, rows)
            seat = random.randint(1, seats_in_row)

        ticket = Ticket(
            row=row,
            seat=seat,
            flight=current_flights,
            order=random.choice(orders),
        )

        ticket_objects.append(ticket)

    Ticket.objects.bulk_create(ticket_objects)

    print(f"Tickets added successfully: {user_input}")

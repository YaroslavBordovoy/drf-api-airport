import random

from django.contrib.auth import get_user_model

from airport.models import Order


def add_orders(user_input: int = 10) -> None:
    users = get_user_model().objects.all()

    order_objects = [
        Order(
            user=random.choice(users)
        )
        for _ in range(user_input)
    ]

    Order.objects.bulk_create(order_objects)

    print("Orders added successfully")

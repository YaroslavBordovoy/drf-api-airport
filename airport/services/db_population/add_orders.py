import random

from django.contrib.auth import get_user_model

from airport.models import Order


def add_orders(user_input: int) -> None:
    users = get_user_model().objects.all()

    order_objects = [
        Order(
            user=random.choice(users)
        )
        for _ in range(user_input)
    ]

    Order.objects.bulk_create(order_objects)

    print(f"Orders added successfully: {user_input}")

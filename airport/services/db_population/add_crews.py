import random

from faker import Faker

from airport.models import Crew


fake = Faker()


def add_crews(user_input: int) -> None:
    roles = ["P", "CP", "FA"]
    crew_objects = [
        Crew(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=random.choice(roles),
        )
        for _ in range(user_input)
    ]

    Crew.objects.bulk_create(crew_objects)

    print(f"Crews added successfully: {user_input}")

from django.contrib.auth.hashers import make_password
from faker import Faker

from accounts.models import User

fake = Faker()


def add_users() -> None:
    user_objects = [
        User(
            password=make_password(fake.password()),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            is_staff=False,
            is_active=True,
        )
        for _ in range(10)
    ]

    User.objects.bulk_create(user_objects)

    print("Users added successfully: 10")

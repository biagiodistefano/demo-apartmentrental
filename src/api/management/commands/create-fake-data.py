import random
import typing as t
from argparse import ArgumentParser

from api.models import Apartment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Create fake data."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--realtors", default=10, type=int, help="Number of realtors to create")
        parser.add_argument("--users", default=10, type=int, help="Number of users to create")
        parser.add_argument("--apartments", default=1000, type=int, help="Number of apartments to create")

    def handle(self, *args: t.Any, **options: t.Any) -> None:
        user_model = get_user_model()
        realtor_group, _ = Group.objects.get_or_create(name="realtor")
        realtors = []
        for x in range(1, options["realtors"] + 1):
            _realtor = user_model.objects.create_user(
                username=f"realtor{x}@example.com",
                email=f"realtor{x}@example.com",
                password="1234",
            )
            realtor_group.user_set.add(_realtor)
            realtors.append(_realtor)

        users_to_create = [
            user_model(username=f"user{x}@example.com", email=f"user{x}@example.com", password="1234")
            for x in range(1, options["users"] + 1)
        ]
        user_model.objects.bulk_create(users_to_create)

        fake = Faker()

        for _ in range(1, options["apartments"] + 1):
            Apartment.objects.create(
                realtor_id=random.choice(realtors).id,
                title=fake.sentence(),
                description=fake.paragraph(),
                area=random.randint(20, 200),
                rooms_no=random.randint(1, 10),
                price_month=random.randint(200, 2000),
                currency="EUR",
            )
        self.stdout.write(self.style.SUCCESS("Created fake data."))

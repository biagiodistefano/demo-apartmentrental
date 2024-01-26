import typing as t
from argparse import ArgumentParser

from decouple import config
from django.contrib.auth import get_user_model
from django.core import management
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Bootstrap the server."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--no-migrate", action="store_true", help="Run migrations")

    def handle(self, *args: t.Any, **options: t.Any) -> None:
        if not options["no_migrate"]:
            management.call_command("migrate", no_input=True)
        try:
            user_model = get_user_model()
            _admin = user_model.objects.create_superuser(
                username=config("SUPERUSER_NAME", default="admin"),
                email="admin@demoapartments.io",
                password=config("SUPERUSER_PASSWORD", default="admin"),
            )
            self.stdout.write(self.style.SUCCESS("Created superuser."))
            if config("SUPERUSER_PASSWORD", default="admin") == "admin":
                self.stdout.write(
                    self.style.WARNING(
                        "WARNING: You are using the default password for the superuser. "
                        "Please change this immediately."
                    )
                )
        except IntegrityError:
            self.stdout.write(self.style.WARNING("Superuser already exists."))

import typing as t

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Apartment


@receiver(post_save, sender=Apartment)
def validate_realtor_group(sender: t.Type[Model], instance: Apartment, **kwargs: t.Any) -> None:
    """
    This signal ensures that all realtors are in the realtor group.
    """

    realtor_group, _ = Group.objects.get_or_create(name="realtor")
    if not instance.realtor.groups.filter(name="realtor").exists():
        raise ValidationError(
            f"User {instance.realtor.username} is not in the realtor group but is assigned as a realtor."
        )

import pytest
from api.models import Apartment
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.core import exceptions


@pytest.fixture
def realtor_user(django_user_model) -> get_user_model():  # type: ignore
    return django_user_model.objects.create_user(
        username="realtor_user", email="realtor@example.com", password="testpass123"
    )


@pytest.fixture
def realtor_group() -> Group:
    group, _ = Group.objects.get_or_create(name="realtor")
    return group


def create_apartment(realtor_user: User) -> Apartment:
    return Apartment.objects.create(
        realtor=realtor_user,
        title="Title",
        description="Description",
        area=100,
        rooms_no=4,
        price_month=1000,
        currency="EUR",
    )


@pytest.mark.django_db
def test_validate_realtor_group_with_realtor_in_group(
    realtor_user: User,
    realtor_group: Group,
) -> None:
    realtor_group.user_set.add(realtor_user)
    create_apartment(realtor_user)


@pytest.mark.django_db
def test_validate_realtor_group_with_realtor_not_in_group(realtor_user: User) -> None:
    realtor_user.groups.clear()
    with pytest.raises(exceptions.ValidationError):
        create_apartment(realtor_user)

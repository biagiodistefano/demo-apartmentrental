from typing import Type

import pytest
from django.contrib.auth.models import Group, User
from django.test import Client


@pytest.fixture
@pytest.mark.django_db
def realtor1(django_user_model: Type[User]) -> User:
    user = django_user_model.objects.create_user(
        username="realtor1@example.com", email="realtor1@example.com", password="123456789"
    )
    realtors, _ = Group.objects.get_or_create(name="realtor")
    realtors.user_set.add(user)
    return user


@pytest.fixture
@pytest.mark.django_db
def realtor2(django_user_model: Type[User]) -> User:
    user = django_user_model.objects.create_user(
        username="realtor2@example.com", email="realtor2@example.com", password="123456789"
    )
    realtors, _ = Group.objects.get_or_create(name="realtor")
    realtors.user_set.add(user)
    return user


@pytest.fixture
def authenticated_realtor_client(client: Client, realtor1: User) -> Client:
    res = client.post(
        "/api/token/pair",
        data={"username": realtor1.username, "password": "123456789"},
        content_type="application/json",
    )
    assert res.status_code == 200
    token = res.json()["access"]
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client


@pytest.fixture
def authenticated_user_client(client: Client, django_user_model: User) -> Client:
    user = django_user_model.objects.create_user(
        username="user@example.com", email="realtor1@example.com", password="123456789"
    )
    res = client.post(
        "/api/token/pair",
        data={"username": user.username, "password": "123456789"},
        content_type="application/json",
    )
    assert res.status_code == 200
    token = res.json()["access"]
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client

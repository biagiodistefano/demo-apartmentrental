import pytest
from django.test import Client
from .helpers import create_test_apartment
from django.contrib.auth.models import User
from api.models import Apartment
from django.shortcuts import reverse
import json


@pytest.fixture
@pytest.mark.django_db
def test_apartments(realtor1: User) -> list[Apartment]:
    return [
        create_test_apartment(
            realtor1, title="Fancy apartment", price_month=1000, currency="EUR", area=100, rooms_no=4
        ),
        create_test_apartment(realtor1, title="Cheap apartment", price_month=300, currency="EUR", area=50, rooms_no=2),
        create_test_apartment(
            realtor1,
            title="Expensive apartment",
            price_month=2000,
            currency="EUR",
            area=150,
            rooms_no=5,
            description="Fantastic apartment",
        ),
    ]


@pytest.mark.django_db
def test_view_apartment(authenticated_user_client: Client, test_apartments: list[Apartment]) -> None:
    res = authenticated_user_client.get(reverse("api:view_apartment", kwargs={"apartment_id": test_apartments[0].id}))
    assert res.status_code == 200
    assert res.json()["title"] == "Fancy apartment"


@pytest.mark.django_db
def test_search_apartments_all(authenticated_user_client: Client, test_apartments: list[Apartment]) -> None:
    res = authenticated_user_client.post(reverse("api:search_apartments"), content_type="application/json")
    assert res.status_code == 200
    assert len(res.json()["results"]) == 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    ["search_payload", "expected_results_titles"],
    [
        ({"price_month__gte": 1000}, ["Fancy apartment", "Expensive apartment"]),
        ({"price_month__lte": 1000}, ["Fancy apartment", "Cheap apartment"]),
        ({"area__gte": 100}, ["Fancy apartment", "Expensive apartment"]),
        ({"area__lte": 50}, ["Cheap apartment"]),
        ({"rooms_no__gte": 4}, ["Fancy apartment", "Expensive apartment"]),
        ({"rooms_no__lte": 4}, ["Cheap apartment", "Fancy apartment"]),
        ({"title": "Fancy"}, ["Fancy apartment"]),
        ({"price_month__lte": 1000, "rooms_no__gt": 5}, []),
        ({"description": "fantastic"}, ["Expensive apartment"]),
    ],
)
def test_search_apartments(
    authenticated_user_client: Client,
    test_apartments: list[Apartment],
    search_payload: dict,
    expected_results_titles: list[str],
) -> None:
    res = authenticated_user_client.post(
        reverse("api:search_apartments"),
        data=json.dumps(search_payload),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert len(res.json()["results"]) == len(expected_results_titles)
    assert all([result["title"] in expected_results_titles for result in res.json()["results"]])

import json

import pytest
from api.models import Apartment
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

from .helpers import create_test_apartment


HERE = Path(__file__).parent.resolve()


@pytest.mark.django_db
def test_realtor_create_apartment_unauthenticated_401(client: Client) -> None:
    response = client.post(
        reverse("api:create_apartment"),
        data=json.dumps(
            {"title": "string", "description": "string", "area": 0, "rooms_no": 0, "price_month": 0, "currency": "EUR"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_realtor_create_apartment_403(authenticated_user_client: Client) -> None:
    response = authenticated_user_client.post(
        reverse("api:create_apartment"),
        data=json.dumps(
            {"title": "string", "description": "string", "area": 0, "rooms_no": 0, "price_month": 0, "currency": "EUR"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_realtor_create_apartment(authenticated_realtor_client: Client) -> None:
    response = authenticated_realtor_client.post(
        reverse("api:create_apartment"),
        data=json.dumps(
            {"title": "string", "description": "string", "area": 0, "rooms_no": 0, "price_month": 0, "currency": "EUR"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_realtor_update_apartment(authenticated_realtor_client: Client, realtor1: User) -> None:
    apartment = create_test_apartment(realtor1)
    response = authenticated_realtor_client.put(
        reverse("api:update_apartment", kwargs={"apartment_id": apartment.id}),
        data=json.dumps(
            {"title": "New Title", "description": "New Description", "price_month": 1500, "currency": "EUR"}
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


@pytest.mark.django_db
def test_realtor_update_apartment_403(authenticated_realtor_client: Client, realtor2: User) -> None:
    apartment = create_test_apartment(realtor2)
    response = authenticated_realtor_client.put(
        reverse("api:update_apartment", kwargs={"apartment_id": apartment.id}),
        data=json.dumps(
            {
                "title": "New Title",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_realtor_set_apartment_image(authenticated_realtor_client: Client, realtor1: User) -> None:
    image = SimpleUploadedFile("image.png", b"file_content", content_type="application/png")
    apartment = create_test_apartment(realtor1)
    response = authenticated_realtor_client.post(
        reverse("api:set_apartment_image", kwargs={"apartment_id": apartment.id}),
        data={"image": image},
    )
    assert response.status_code == 200
    assert Apartment.objects.get(id=apartment.id).preview_image


@pytest.mark.django_db
def test_realtor_set_apartment_image_403(authenticated_realtor_client: Client, realtor2: User) -> None:
    image = SimpleUploadedFile("image.png", b"file_content", content_type="application/png")
    apartment = create_test_apartment(realtor2)
    response = authenticated_realtor_client.post(
        reverse("api:set_apartment_image", kwargs={"apartment_id": apartment.id}),
        data={"image": image},
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_realtor_get_all_own_apartments(authenticated_realtor_client: Client, realtor1: User, realtor2: User) -> None:
    for _ in range(60):
        create_test_apartment(realtor1)
    for _ in range(5):
        create_test_apartment(realtor2)
    total = Apartment.objects.filter(realtor_id=realtor1.id).count()
    response = authenticated_realtor_client.get(reverse("api:get_all_own_apartments"))
    assert response.status_code == 200
    count = response.json()["count"]
    assert count == total


@pytest.mark.django_db
def test_realtor_delete_apartment(authenticated_realtor_client: Client, realtor1: User) -> None:
    apartment = create_test_apartment(realtor1)
    response = authenticated_realtor_client.delete(
        reverse("api:delete_apartment", kwargs={"apartment_id": apartment.id})
    )
    assert response.status_code == 204
    assert not Apartment.objects.filter(id=apartment.id).exists()


@pytest.mark.django_db
def test_realtor_delete_apartment_403(authenticated_realtor_client: Client, realtor2: User) -> None:
    apartment = create_test_apartment(realtor2)
    response = authenticated_realtor_client.delete(
        reverse("api:delete_apartment", kwargs={"apartment_id": apartment.id})
    )
    assert response.status_code == 403
    assert Apartment.objects.filter(id=apartment.id).exists()

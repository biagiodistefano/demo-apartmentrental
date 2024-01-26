import json

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


@pytest.mark.django_db
def test_registration_success(client: Client) -> None:
    response = client.post(
        reverse("api:user_registration"),
        data=json.dumps(
            {
                "email": "email@example.com",
                "password1": "P+Z5VFozhvbzJ4dI+HzGUQ==",
                "password2": "P+Z5VFozhvbzJ4dI+HzGUQ==",
                "is_realtor": True,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 201
    response = client.post(
        "/api/token/pair",
        data={"username": "email@example.com", "password": "P+Z5VFozhvbzJ4dI+HzGUQ=="},
        content_type="application/json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_password_too_short(client: Client) -> None:
    response = client.post(
        reverse("api:user_registration"),
        data=json.dumps(
            {
                "email": "email@example.com",
                "password1": "12345",
                "password2": "12345",
                "is_realtor": True,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_mismatching_passwords(client: Client) -> None:
    response = client.post(
        reverse("api:user_registration"),
        data=json.dumps(
            {
                "email": "email@example.com",
                "password1": "P+Z5VFozhvbzJ4dI+HzGUQ==",
                "password2": "P+Z5VFozhvbzJ4dI+HzGUQ",
                "is_realtor": True,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 422


@pytest.mark.django_db
def test_registration_fail_user_exists(client: Client) -> None:
    get_user_model().objects.create_user(username="existing@example.com", password="123456789")
    response = client.post(
        reverse("api:user_registration"),
        data=json.dumps(
            {
                "email": "existing@example.com",
                "password1": "P+Z5VFozhvbzJ4dI+HzGUQ==",
                "password2": "P+Z5VFozhvbzJ4dI+HzGUQ==",
                "is_realtor": True,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 400

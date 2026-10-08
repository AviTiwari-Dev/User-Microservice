"""
Tests the update-user API endpoint.
"""

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid7

from fastapi import status


def test_patch_user(client, user_manager_override):
    user_id = uuid7()

    updated_user = MagicMock()

    updated_user.user_id = user_id
    updated_user.first_name = "avi"
    updated_user.middle_name = ""
    updated_user.last_name = "tiwari"
    updated_user.date_of_birth = date(1997, 1, 1)
    updated_user.gender = "male"

    user_manager_override.update.return_value = updated_user

    response = client.patch(
        f"/api/v1/user/{user_id}",
        json={
            "first_name": "Avi",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["user_id"] == str(user_id)
    assert data["first_name"] == "avi"
    assert data["middle_name"] == ""
    assert data["last_name"] == "tiwari"
    assert data["date_of_birth"] == "1997-01-01"
    assert data["gender"] == "male"

    user_manager_override.update.assert_awaited_once()

    call_kwargs = user_manager_override.update.await_args.kwargs

    assert call_kwargs["user_id"] == user_id

    request = call_kwargs["request"]

    assert request.first_name == "avi"
    assert request.middle_name == ""
    assert request.last_name == "tiwari"
    assert request.date_of_birth == date(1997, 1, 1)
    assert request.gender.value == "male"


def test_patch_user_invalid_uuid(
    client,
    user_manager_override,
):
    response = client.patch(
        "/api/v1/user/not-a-valid-uuid",
        json={
            "first_name": "Avi",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.update.assert_not_awaited()


def test_patch_user_invalid_first_name(
    client,
    user_manager_override,
):
    user_id = uuid7()

    response = client.patch(
        f"/api/v1/user/{user_id}",
        json={
            "first_name": "Avi123",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.update.assert_not_awaited()


def test_patch_user_extra_field(
    client,
    user_manager_override,
):
    user_id = uuid7()

    response = client.patch(
        f"/api/v1/user/{user_id}",
        json={
            "first_name": "Avi",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
            "unknown_field": "something",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.update.assert_not_awaited()


def test_patch_user_partial_update(
    client,
    user_manager_override,
):
    user_id = uuid7()

    updated_user = MagicMock()

    updated_user.user_id = user_id
    updated_user.first_name = "avi"
    updated_user.middle_name = ""
    updated_user.last_name = "tiwari"
    updated_user.date_of_birth = date(1997, 1, 1)
    updated_user.gender = "male"

    user_manager_override.update.return_value = updated_user

    response = client.patch(
        f"/api/v1/user/{user_id}",
        json={
            "first_name": "Avi",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["user_id"] == str(user_id)
    assert data["first_name"] == "avi"

    user_manager_override.update.assert_awaited_once()

    call_kwargs = user_manager_override.update.await_args.kwargs

    assert call_kwargs["user_id"] == user_id
    assert call_kwargs["request"].first_name == "avi"
    assert call_kwargs["request"].date_of_birth is None

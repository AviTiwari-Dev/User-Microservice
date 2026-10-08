"""
Tests the get-user-by-id API endpoint.
"""

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid7

from fastapi import status


def test_get_user(client, user_manager_override):
    user_id = uuid7()

    user = MagicMock()

    user.user_id = user_id
    user.first_name = "avi"
    user.middle_name = ""
    user.last_name = "tiwari"
    user.date_of_birth = date(1997, 1, 1)
    user.gender = "male"

    user_manager_override.get_by_user_id.return_value = user

    response = client.get(
        f"/api/v1/user/{user_id}",
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["user_id"] == str(user_id)
    assert data["first_name"] == "avi"
    assert data["middle_name"] == ""
    assert data["last_name"] == "tiwari"
    assert data["date_of_birth"] == "1997-01-01"
    assert data["gender"] == "male"

    user_manager_override.get_by_user_id.assert_awaited_once_with(user_id)


def test_get_user_invalid_uuid(
    client,
    user_manager_override,
):
    response = client.get(
        "/api/v1/user/not-a-valid-uuid",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.get_by_user_id.assert_not_awaited()

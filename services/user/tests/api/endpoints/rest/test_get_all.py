"""
Tests the get-users API endpoint.
"""

from datetime import date
from unittest.mock import MagicMock
from uuid import uuid7

from fastapi import status


def test_get_users(client, user_manager_override):
    response = client.get(
        "/api/v1/user/",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    user_manager_override.get_all.assert_awaited_once_with(
        cursor=None,
        limit=100,
    )


def test_get_users_with_users(client, user_manager_override):
    user_1 = MagicMock()
    user_1.user_id = uuid7()
    user_1.first_name = "avi"
    user_1.middle_name = ""
    user_1.last_name = "tiwari"
    user_1.date_of_birth = date(1997, 1, 1)
    user_1.gender = "male"

    user_2 = MagicMock()
    user_2.user_id = uuid7()
    user_2.first_name = "rahul"
    user_2.middle_name = ""
    user_2.last_name = "sharma"
    user_2.date_of_birth = date(1996, 5, 15)
    user_2.gender = "male"

    user_manager_override.get_all.return_value = [
        user_1,
        user_2,
    ]

    response = client.get(
        "/api/v1/user/",
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 2

    assert data[0]["user_id"] == str(user_1.user_id)
    assert data[0]["first_name"] == "avi"
    assert data[0]["last_name"] == "tiwari"

    assert data[1]["user_id"] == str(user_2.user_id)
    assert data[1]["first_name"] == "rahul"
    assert data[1]["last_name"] == "sharma"

    user_manager_override.get_all.assert_awaited_once_with(
        cursor=None,
        limit=100,
    )


def test_get_users_with_limit(client, user_manager_override):
    response = client.get(
        "/api/v1/user/?limit=25",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    user_manager_override.get_all.assert_awaited_once_with(
        cursor=None,
        limit=25,
    )


def test_get_users_with_cursor(client, user_manager_override):
    cursor = uuid7()

    response = client.get(
        f"/api/v1/user/?cursor={cursor}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    user_manager_override.get_all.assert_awaited_once_with(
        cursor=cursor,
        limit=100,
    )


def test_get_users_with_cursor_and_limit(
    client,
    user_manager_override,
):
    cursor = uuid7()

    response = client.get(
        f"/api/v1/user/?cursor={cursor}&limit=50",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

    user_manager_override.get_all.assert_awaited_once_with(
        cursor=cursor,
        limit=50,
    )


def test_get_users_invalid_cursor(
    client,
    user_manager_override,
):
    response = client.get(
        "/api/v1/user/?cursor=invalid-uuid",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.get_all.assert_not_awaited()


def test_get_users_limit_less_than_one(
    client,
    user_manager_override,
):
    response = client.get(
        "/api/v1/user/?limit=0",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.get_all.assert_not_awaited()


def test_get_users_limit_greater_than_one_hundred(
    client,
    user_manager_override,
):
    response = client.get(
        "/api/v1/user/?limit=101",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.get_all.assert_not_awaited()

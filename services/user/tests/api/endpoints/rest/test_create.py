"""
Tests the create-user API endpoint.
"""

from fastapi import status


def test_create_user(client, user_manager_override):
    response = client.post(
        "/api/v1/user/",
        json={
            "first_name": "Avi",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    created_user = user_manager_override.create.return_value

    assert data["user_id"] == str(created_user.user_id)
    assert data["first_name"] == "avi"
    assert data["middle_name"] == ""
    assert data["last_name"] == "tiwari"
    assert data["date_of_birth"] == "1997-01-01"
    assert data["gender"] == "male"

    user_manager_override.create.assert_awaited_once()


def test_create_user_invalid_first_name(client):
    response = client.post(
        "/api/v1/user/",
        json={
            "first_name": "Avi123",
            "middle_name": "",
            "last_name": "Tiwari",
            "date_of_birth": "1997-01-01",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_missing_field(client):
    response = client.post(
        "/api/v1/user/",
        json={
            "first_name": "Avi",
            "middle_name": "",
            "last_name": "Tiwari",
            "gender": "male",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_extra_field(client):
    response = client.post(
        "/api/v1/user/",
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

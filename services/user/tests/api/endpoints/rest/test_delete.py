"""
Tests the delete-user API endpoint.
"""

from uuid import uuid7

from fastapi import status


def test_delete_user(client, user_manager_override):
    user_id = uuid7()

    response = client.delete(
        f"/api/v1/user/{user_id}",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    user_manager_override.delete.assert_awaited_once_with(user_id)


def test_delete_user_invalid_uuid(client, user_manager_override):
    response = client.delete(
        "/api/v1/user/not-a-valid-uuid",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    user_manager_override.delete.assert_not_awaited()


def test_delete_user_missing_uuid(client, user_manager_override):
    response = client.delete(
        "/api/v1/user/",
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    user_manager_override.delete.assert_not_awaited()

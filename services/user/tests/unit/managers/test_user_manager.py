"""
Tests the UserManager business logic.
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid7

import pytest

from services.user.src.enums.gender import GenderEnum
from services.user.src.exceptions.user_not_found_error import (
    UserNotFoundError,
)
from services.user.src.managers.implementations.user import UserManager
from services.user.src.models.data_validation.user_request_base import (
    UserRequestBase,
)
from services.user.src.models.data_validation.user_request_update_base import (
    UserRequestUpdateBase,
)


@pytest.mark.asyncio
async def test_create(
    manager,
    repository,
    user_request,
    user,
):
    repository.create.return_value = user

    result = await manager.create(user_request)

    assert result is user

    repository.create.assert_awaited_once()

    created_user = repository.create.await_args.args[0]

    assert created_user.first_name == "avi"
    assert created_user.middle_name == ""
    assert created_user.last_name == "tiwari"
    assert created_user.date_of_birth == date(1997, 1, 1)
    assert created_user.gender == "male"


@pytest.mark.asyncio
async def test_get_by_user_id(
    manager,
    repository,
    user,
):
    user_id = user.user_id

    repository.get_by_user_id.return_value = user

    result = await manager.get_by_user_id(user_id)

    assert result is user

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )


@pytest.mark.asyncio
async def test_get_by_user_id_not_found(
    manager,
    repository,
):
    user_id = uuid7()

    repository.get_by_user_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await manager.get_by_user_id(user_id)

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )


@pytest.mark.asyncio
async def test_get_all(
    manager,
    repository,
    user,
):
    cursor = uuid7()
    limit = 25

    repository.get_all.return_value = [user]

    result = await manager.get_all(
        cursor=cursor,
        limit=limit,
    )

    assert result == [user]

    repository.get_all.assert_awaited_once_with(
        cursor=cursor,
        limit=limit,
    )


@pytest.mark.asyncio
async def test_get_all_with_defaults(
    manager,
    repository,
):
    repository.get_all.return_value = []

    result = await manager.get_all()

    assert result == []

    repository.get_all.assert_awaited_once_with(
        cursor=None,
        limit=100,
    )


@pytest.mark.asyncio
async def test_update(
    manager,
    repository,
    update_request,
    user,
):
    user_id = user.user_id

    repository.get_by_user_id.return_value = user
    repository.update.return_value = user

    result = await manager.update(
        user_id=user_id,
        request=update_request,
    )

    assert result is user

    assert user.first_name == "rahul"
    assert user.middle_name == ""
    assert user.last_name == "tiwari"
    assert user.date_of_birth == date(1997, 1, 1)
    assert user.gender == "male"

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )

    repository.update.assert_awaited_once_with(
        user,
    )


@pytest.mark.asyncio
async def test_update_partial_fields(
    manager,
    repository,
    user,
):
    user_id = user.user_id

    update_request = UserRequestUpdateBase(
        last_name="Sharma",
        gender=GenderEnum.FEMALE,
    )

    repository.get_by_user_id.return_value = user
    repository.update.return_value = user

    result = await manager.update(
        user_id=user_id,
        request=update_request,
    )

    assert result is user

    assert user.first_name == "avi"
    assert user.middle_name == ""
    assert user.last_name == "sharma"
    assert user.date_of_birth == date(1997, 1, 1)
    assert user.gender == "female"

    repository.update.assert_awaited_once_with(
        user,
    )


@pytest.mark.asyncio
async def test_update_user_not_found(
    manager,
    repository,
    update_request,
):
    user_id = uuid7()

    repository.get_by_user_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await manager.update(
            user_id=user_id,
            request=update_request,
        )

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )

    repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_delete(
    manager,
    repository,
    user,
):
    user_id = user.user_id

    repository.get_by_user_id.return_value = user

    result = await manager.delete(user_id)

    assert result is None

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )

    repository.delete.assert_awaited_once_with(
        user,
    )


@pytest.mark.asyncio
async def test_delete_user_not_found(
    manager,
    repository,
):
    user_id = uuid7()

    repository.get_by_user_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await manager.delete(user_id)

    repository.get_by_user_id.assert_awaited_once_with(
        user_id,
    )

    repository.delete.assert_not_awaited()

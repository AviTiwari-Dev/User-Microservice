from datetime import date
from uuid import uuid7

import pytest

from services.user.src.enums.gender import GenderEnum
from services.user.src.exceptions.user_not_found_error import (
    UserNotFoundError,
)
from services.user.src.models.data_storage.user import User


@pytest.mark.asyncio
async def test_create(
    repository,
):
    user = User(
        first_name="avi",
        middle_name="",
        last_name="tiwari",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )

    created_user = await repository.create(user)

    assert created_user.user_id is not None
    assert created_user.first_name == "avi"
    assert created_user.middle_name == ""
    assert created_user.last_name == "tiwari"
    assert created_user.date_of_birth == date(1997, 1, 1)
    assert created_user.gender is GenderEnum.MALE
    assert created_user.created_at is not None
    assert created_user.updated_at is not None

    await repository.delete(created_user)


@pytest.mark.asyncio
async def test_get_by_user_id(
    repository,
    user,
):
    result = await repository.get_by_user_id(
        user.user_id,
    )

    assert result is not None
    assert result.user_id == user.user_id
    assert result.first_name == "avi"
    assert result.last_name == "tiwari"


@pytest.mark.asyncio
async def test_get_by_user_id_not_found(
    repository,
):
    result = await repository.get_by_user_id(
        uuid7(),
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_by_user_id_include_deleted(
    repository,
    user,
):
    await repository.delete(user)

    result = await repository.get_by_user_id(
        user.user_id,
        include_deleted=True,
    )

    assert result is not None
    assert result.user_id == user.user_id
    assert result.deleted_at is not None


@pytest.mark.asyncio
async def test_get_by_user_id_excludes_deleted(
    repository,
    user,
):
    user_id = user.user_id

    await repository.delete(user)

    result = await repository.get_by_user_id(
        user_id,
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_all(
    repository,
):
    users = [
        User(
            first_name=f"avi{i}",
            middle_name="",
            last_name="tiwari",
            date_of_birth=date(1997, 1, 1),
            gender=GenderEnum.MALE,
        )
        for i in range(3)
    ]

    for user in users:
        await repository.create(user)

    result = await repository.get_all(
        limit=3,
    )

    assert len(result) == 3
    assert result == sorted(
        result,
        key=lambda user: user.user_id,
    )

    for user in users:
        await repository.delete(user)


@pytest.mark.asyncio
async def test_get_all_with_cursor(
    repository,
):
    users = [
        User(
            first_name=f"avi{i}",
            middle_name="",
            last_name="tiwari",
            date_of_birth=date(1997, 1, 1),
            gender=GenderEnum.MALE,
        )
        for i in range(3)
    ]

    for user in users:
        await repository.create(user)

    first_page = await repository.get_all(
        limit=2,
    )

    assert len(first_page) == 2

    second_page = await repository.get_all(
        cursor=first_page[-1].user_id,
        limit=2,
    )

    assert len(second_page) == 1
    assert second_page[0].user_id > first_page[-1].user_id

    for user in users:
        await repository.delete(user)


@pytest.mark.asyncio
async def test_get_all_excludes_deleted_users(
    repository,
):
    active_user = User(
        first_name="active",
        middle_name="",
        last_name="user",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )

    deleted_user = User(
        first_name="deleted",
        middle_name="",
        last_name="user",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )

    await repository.create(active_user)
    await repository.create(deleted_user)

    await repository.delete(deleted_user)

    result = await repository.get_all(
        limit=100,
    )

    result_ids = {user.user_id for user in result}

    assert active_user.user_id in result_ids
    assert deleted_user.user_id not in result_ids

    await repository.delete(active_user)


@pytest.mark.asyncio
async def test_update(
    repository,
    user,
):
    user.first_name = "updated"
    user.last_name = "name"

    updated_user = await repository.update(user)

    assert updated_user.user_id == user.user_id
    assert updated_user.first_name == "updated"
    assert updated_user.last_name == "name"

    result = await repository.get_by_user_id(
        user.user_id,
    )

    assert result is not None
    assert result.first_name == "updated"
    assert result.last_name == "name"


@pytest.mark.asyncio
async def test_update_user_not_found(
    repository,
):
    user = User(
        user_id=uuid7(),
        first_name="avi",
        middle_name="",
        last_name="tiwari",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )

    with pytest.raises(UserNotFoundError):
        await repository.update(user)


@pytest.mark.asyncio
async def test_update_deleted_user(
    repository,
    user,
):
    user_id = user.user_id

    await repository.delete(user)

    user_update = User(
        user_id=user_id,
        first_name="updated",
        middle_name="",
        last_name="tiwari",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )

    with pytest.raises(UserNotFoundError):
        await repository.update(user_update)

    result = await repository.get_by_user_id(
        user_id,
        include_deleted=True,
    )

    assert result is not None
    assert result.first_name == "avi"
    assert result.deleted_at is not None


@pytest.mark.asyncio
async def test_delete(
    repository,
    user,
):
    user_id = user.user_id

    await repository.delete(user)

    result = await repository.get_by_user_id(
        user_id,
    )

    assert result is None

    deleted_user = await repository.get_by_user_id(
        user_id,
        include_deleted=True,
    )

    assert deleted_user is not None
    assert deleted_user.deleted_at is not None

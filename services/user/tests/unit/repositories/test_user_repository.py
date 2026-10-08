"""
Tests the PostgreSQL user repository.
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid7

import pytest

from services.user.src.exceptions.user_not_found_error import (
    UserNotFoundError,
)
from services.user.src.models.data_storage.user import User
from services.user.src.repositories.implementation.postgresql.user import (
    PostgresqlUserRepository,
)


@pytest.fixture
def session():
    """
    Provides a mocked asynchronous database session.
    """
    session = MagicMock()

    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()

    return session


@pytest.fixture
def repository(session):
    """
    Provides a PostgreSQL user repository using the mocked session.
    """
    return PostgresqlUserRepository(session)


@pytest.fixture
def user():
    """
    Provides a mocked user entity.
    """
    user = MagicMock(spec=User)

    user.user_id = uuid7()

    return user


@pytest.mark.asyncio
async def test_create(
    repository,
    session,
    user,
):
    result = await repository.create(user)

    assert result is user

    session.add.assert_called_once_with(user)
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_get_by_user_id(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    result_mock.scalar_one_or_none.return_value = user

    session.execute.return_value = result_mock

    result = await repository.get_by_user_id(
        user.user_id,
    )

    assert result is user

    session.execute.assert_awaited_once()
    result_mock.scalar_one_or_none.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_by_user_id_not_found(
    repository,
    session,
):
    user_id = uuid7()

    result_mock = MagicMock()

    result_mock.scalar_one_or_none.return_value = None

    session.execute.return_value = result_mock

    result = await repository.get_by_user_id(user_id)

    assert result is None

    session.execute.assert_awaited_once()
    result_mock.scalar_one_or_none.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_by_user_id_include_deleted(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    result_mock.scalar_one_or_none.return_value = user

    session.execute.return_value = result_mock

    result = await repository.get_by_user_id(
        user.user_id,
        include_deleted=True,
    )

    assert result is user

    session.execute.assert_awaited_once()
    result_mock.scalar_one_or_none.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_all(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    result_mock.scalars.return_value = [user]

    session.execute.return_value = result_mock

    result = await repository.get_all(
        limit=25,
    )

    assert result == [user]

    session.execute.assert_awaited_once()
    result_mock.scalars.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_all_with_cursor(
    repository,
    session,
    user,
):
    cursor = uuid7()

    result_mock = MagicMock()

    result_mock.scalars.return_value = [user]

    session.execute.return_value = result_mock

    result = await repository.get_all(
        cursor=cursor,
        limit=25,
    )

    assert result == [user]

    session.execute.assert_awaited_once()
    result_mock.scalars.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_all_empty(
    repository,
    session,
):
    result_mock = MagicMock()

    result_mock.scalars.return_value = []

    session.execute.return_value = result_mock

    result = await repository.get_all()

    assert result == []

    session.execute.assert_awaited_once()
    result_mock.scalars.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_all_limit_is_capped_at_100(
    repository,
    session,
):
    result_mock = MagicMock()

    result_mock.scalars.return_value = []

    session.execute.return_value = result_mock

    result = await repository.get_all(
        limit=500,
    )

    assert result == []

    session.execute.assert_awaited_once()
    result_mock.scalars.assert_called_once_with()


@pytest.mark.asyncio
async def test_update(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    result_mock.scalar_one_or_none.return_value = user.user_id

    session.execute.return_value = result_mock

    result = await repository.update(user)

    assert result is user

    session.execute.assert_awaited_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(user)

    result_mock.scalar_one_or_none.assert_called_once_with()


@pytest.mark.asyncio
async def test_update_user_not_found(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    result_mock.scalar_one_or_none.return_value = None

    session.execute.return_value = result_mock

    with pytest.raises(UserNotFoundError):
        await repository.update(user)

    session.execute.assert_awaited_once()

    session.commit.assert_not_awaited()
    session.refresh.assert_not_awaited()

    result_mock.scalar_one_or_none.assert_called_once_with()


@pytest.mark.asyncio
async def test_delete(
    repository,
    session,
    user,
):
    result_mock = MagicMock()

    session.execute.return_value = result_mock

    await repository.delete(user)

    statement = session.execute.await_args.args[0]

    assert statement.table == User.__table__

    assert statement._values is not None

    session.execute.assert_awaited_once()
    session.commit.assert_awaited_once()

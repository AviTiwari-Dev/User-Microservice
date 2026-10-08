"""
Provides fixtures for unit tests.
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid7

import pytest

from services.user.src.enums.gender import GenderEnum
from services.user.src.managers.implementations.user import UserManager
from services.user.src.models.data_validation.user_request_base import (
    UserRequestBase,
)
from services.user.src.models.data_validation.user_request_update_base import (
    UserRequestUpdateBase,
)


@pytest.fixture
def repository():
    """
    Provides a mocked user repository.
    """
    repository = MagicMock()

    repository.create = AsyncMock()
    repository.get_by_user_id = AsyncMock()
    repository.get_all = AsyncMock()
    repository.update = AsyncMock()
    repository.delete = AsyncMock()

    return repository


@pytest.fixture
def manager(repository):
    """
    Provides a UserManager using the mocked repository.
    """
    return UserManager(repository)


@pytest.fixture
def user_request():
    """
    Provides a valid user creation request.
    """
    return UserRequestBase(
        first_name="Avi",
        middle_name="",
        last_name="Tiwari",
        date_of_birth=date(1997, 1, 1),
        gender=GenderEnum.MALE,
    )


@pytest.fixture
def update_request():
    """
    Provides a valid user update request.
    """
    return UserRequestUpdateBase(
        first_name="Rahul",
    )


@pytest.fixture
def user():
    """
    Provides a mocked user entity.
    """
    user = MagicMock()

    user.user_id = uuid7()
    user.first_name = "avi"
    user.middle_name = ""
    user.last_name = "tiwari"
    user.date_of_birth = date(1997, 1, 1)
    user.gender = GenderEnum.MALE

    return user

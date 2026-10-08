"""
Provides shared pytest fixtures for user-service API tests.
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid7

import pytest
from fastapi.testclient import TestClient

from services.user.src.dependencies.get_user_manager import get_user_manager
from services.user.src.main import user_api


@pytest.fixture
def client():
    """
    Provides a FastAPI test client.
    """
    return TestClient(user_api)


@pytest.fixture
def mock_user_manager():
    """
    Provides a mocked user manager.
    """
    user_id = uuid7()

    created_user = MagicMock()

    created_user.user_id = user_id
    created_user.first_name = "avi"
    created_user.middle_name = ""
    created_user.last_name = "tiwari"
    created_user.date_of_birth = date(1997, 1, 1)
    created_user.gender = "male"

    manager = MagicMock()

    manager.create = AsyncMock(return_value=created_user)

    manager.delete = AsyncMock()

    manager.get_all = AsyncMock(return_value=[])

    manager.get_by_user_id = AsyncMock()

    manager.update = AsyncMock()

    return manager


@pytest.fixture
def user_manager_override(mock_user_manager):
    """
    Overrides the application's user-manager dependency for testing.
    """
    user_api.dependency_overrides[get_user_manager] = lambda: mock_user_manager

    yield mock_user_manager

    user_api.dependency_overrides.clear()

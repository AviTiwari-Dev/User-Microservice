"""
Provides FastAPI dependencies for user-related operations.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..managers.implementations.user import UserManager
from ..managers.interfaces.user import UserManagerProtocol
from ..repositories.implementation.postgresql.user import PostgresqlUserRepository
from .get_session import get_session


async def get_user_manager(
    session: AsyncSession = Depends(get_session),
) -> UserManagerProtocol:
    """
    Create and provide a user manager instance.

    Args:
        session: Database session provided by the session dependency.

    Returns:
        A configured user manager.
    """
    repository = PostgresqlUserRepository(session)

    return UserManager(repository)

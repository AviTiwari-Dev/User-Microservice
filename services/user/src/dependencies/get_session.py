"""
Provides an asynchronous database session for request handling.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..session_factories.user import session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and provide an asynchronous database session.

    A new session is created for each request and is automatically
    closed when the request has completed.

    Yields:
        An active SQLAlchemy asynchronous session.
    """
    async with session_factory() as session:
        yield session

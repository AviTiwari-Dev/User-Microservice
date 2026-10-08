"""
Provides repository methods for performing user-related database operations.
"""

from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ....exceptions.user_not_found_error import UserNotFoundError
from ....models.data_storage.user import User


class PostgresqlUserRepository:
    """
    Repository responsible for managing persistence and retrieval of
    :class:`User` entities.

    Encapsulates all database operations for users, providing a clean
    abstraction between the data access layer and the business logic.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def create(
        self,
        user: User,
    ) -> User:
        """
        Persist a new user in the database.

        Args:
            user: The user entity to create.

        Returns:
            The newly created user with any database-generated values
            populated.
        """
        self._session.add(user)

        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def get_by_user_id(
        self,
        user_id: UUID,
        *,
        include_deleted: bool = False,
    ) -> User | None:
        """
        Retrieve a user by its unique identifier.

        Args:
            user_id: The unique identifier of the user.
            include_deleted: Whether to include soft-deleted users.

        Returns:
            The matching user if found; otherwise, ``None``.
        """
        statement = select(User).where(User.user_id == user_id)

        if not include_deleted:
            statement = statement.where(User.deleted_at.is_(None))

        result = await self._session.execute(statement)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        cursor: UUID | None = None,
        limit: int = 100,
    ) -> list[User]:
        """
        Retrieve a paginated list of active users using cursor pagination.

        Soft-deleted users are excluded from the result set. Results are
        ordered by their unique identifier to provide stable pagination.

        Args:
            cursor: The unique identifier of the last user returned by the
                previous request. If ``None``, pagination starts from the
                beginning.
            limit: Maximum number of users to return (upto 100).

        Returns:
            A list of active users.
        """
        limit = min(limit, 100)
        statement = (
            select(User)
            .where(User.deleted_at.is_(None))
            .order_by(User.user_id)
            .limit(limit)
        )

        if cursor is not None:
            statement = statement.where(User.user_id > cursor)

        result = await self._session.execute(statement)

        return list(result.scalars())

    async def update(
        self,
        user: User,
    ) -> User:
        """
        Persist changes made to an existing active user.

        Args:
            user: The user entity containing updated values.

        Returns:
            The updated user after the session has been committed and
            refreshed.

        Raises:
            UserNotFoundError: If the user does not exist or has been
                soft deleted.
        """
        result = await self._session.execute(
            select(User.user_id).where(
                User.user_id == user.user_id,
                User.deleted_at.is_(None),
            ),
        )

        if result.scalar_one_or_none() is None:
            raise UserNotFoundError()

        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def delete(
        self,
        user: User,
    ) -> None:
        """
        Soft delete a user.

        Args:
            user: The user entity to delete.
        """
        await self._session.execute(
            update(User)
            .where(
                User.user_id == user.user_id,
                User.deleted_at.is_(None),
            )
            .values(
                deleted_at=func.now(),
            )
        )

        await self._session.commit()

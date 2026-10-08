"""
Defines the interface for user persistence operations.
"""

from typing import Protocol
from uuid import UUID

from ...models.data_storage.user import User


class UserRepository(Protocol):
    """
    Defines the contract for user persistence operations.

    Implementations of this protocol are responsible for persisting
    and retrieving :class:`User` entities without exposing the
    underlying storage technology to the business layer.

    The protocol uses structural typing, so an implementation does
    not need to explicitly inherit from this class. It only needs
    to provide the methods defined by this interface.

    Implementations may use PostgreSQL, another database, an
    in-memory data store, or a mock repository for testing.
    """

    async def create(
        self,
        user: User,
    ) -> User:
        """
        Persist a new user.

        Args:
            user: The user entity to persist.

        Returns:
            The persisted user with any database-generated values
            populated.
        """
        ...

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
            include_deleted: Whether soft-deleted users should be
                included in the search.

        Returns:
            The matching user if found; otherwise, ``None``.
        """
        ...

    async def get_all(
        self,
        *,
        cursor: UUID | None = None,
        limit: int = 100,
    ) -> list[User]:
        """
        Retrieve a paginated list of active users.

        Implementations should use cursor-based pagination and
        exclude soft-deleted users.

        Args:
            cursor: The unique identifier of the last user returned
                by the previous request. If ``None``, pagination
                starts from the beginning.
            limit: Maximum number of users to return.

        Returns:
            A list of active users.
        """
        ...

    async def update(
        self,
        user: User,
    ) -> User:
        """
        Persist changes made to an existing active user.

        Args:
            user: The user entity containing the updated values.

        Returns:
            The updated user.

        Raises:
            UserNotFoundError: If the user does not exist or has
                been soft deleted.
        """
        ...

    async def delete(
        self,
        user: User,
    ) -> None:
        """
        Soft delete an active user.

        Args:
            user: The user entity to delete.
        """
        ...

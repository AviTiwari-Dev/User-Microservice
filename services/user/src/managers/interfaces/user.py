"""
Defines the interface for user management operations.
"""

from typing import Protocol
from uuid import UUID

from ...models.data_storage.user import User
from ...models.data_validation.user_request_base import UserRequestBase
from ...models.data_validation.user_request_update_base import (
    UserRequestUpdateBase,
)


class UserManagerProtocol(Protocol):
    """
    Defines the contract for user management operations.

    This protocol represents the public interface exposed by the
    user management layer. Implementations are responsible for
    applying business rules and coordinating user persistence
    through an appropriate repository.

    Implementations do not need to explicitly inherit from this
    protocol. Any class that provides compatible implementations
    of the declared methods satisfies the protocol through
    structural typing.

    The protocol intentionally exposes only business operations
    required by consumers such as API endpoints. Repository
    details and implementation-specific methods are not part
    of this contract.
    """

    async def create(
        self,
        request: UserRequestBase,
    ) -> User:
        """
        Create a new user.

        Args:
            request: Validated user creation data.

        Returns:
            The newly created user.
        """
        ...

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> User:
        """
        Retrieve an active user by its unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The matching active user.

        Raises:
            UserNotFoundError: If the user does not exist or has
                been soft deleted.
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

        Args:
            cursor: The unique identifier of the last user
                returned by the previous request. If ``None``,
                pagination starts from the beginning.
            limit: Maximum number of users to return.

        Returns:
            A list of active users.
        """
        ...

    async def update(
        self,
        user_id: UUID,
        request: UserRequestUpdateBase,
    ) -> User:
        """
        Update an existing active user.

        Args:
            user_id: The unique identifier of the user.
            request: Validated user update data.

        Returns:
            The updated user.

        Raises:
            UserNotFoundError: If the user does not exist or has
                been soft deleted.
        """
        ...

    async def delete(
        self,
        user_id: UUID,
    ) -> None:
        """
        Soft delete an active user.

        Args:
            user_id: The unique identifier of the user.

        Raises:
            UserNotFoundError: If the user does not exist or has
                been soft deleted.
        """
        ...

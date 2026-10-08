"""
Provides business logic for managing users.
"""

from uuid import UUID

from ...exceptions.user_not_found_error import UserNotFoundError
from ...models.data_storage.user import User
from ...models.data_validation.user_request_base import UserRequestBase
from ...models.data_validation.user_request_update_base import (
    UserRequestUpdateBase,
)
from ...repositories.interfaces.user import UserRepository


class UserManager:
    """
    Manages user-related business operations.

    Coordinates validation and persistence of user entities by using the
    user repository.
    """

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        """
        Initialize the user manager.

        Args:
            repository: Repository used to access user data.
        """
        self._repository = repository

    async def create(
        self,
        request: UserRequestBase,
    ) -> User:
        """
        Create a new user.

        Args:
            request: User creation request.

        Returns:
            The newly created user.
        """
        user = User(
            first_name=request.first_name,
            middle_name=request.middle_name,
            last_name=request.last_name,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
        )

        return await self._repository.create(user)

    async def get_by_user_id(
        self,
        user_id: UUID,
    ) -> User:
        """
        Retrieve an active user by its unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The matching user.

        Raises:
            UserNotFoundError: If the user does not exist or has been
                soft deleted.
        """
        user = await self._repository.get_by_user_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def get_all(
        self,
        *,
        cursor: UUID | None = None,
        limit: int = 100,
    ) -> list[User]:
        """
        Retrieve a paginated list of active users.

        Args:
            cursor: Pagination cursor.
            limit: Maximum number of users to return.

        Returns:
            A list of users.
        """
        return await self._repository.get_all(
            cursor=cursor,
            limit=limit,
        )

    async def update(
        self,
        user_id: UUID,
        request: UserRequestUpdateBase,
    ) -> User:
        """
        Update an existing user.

        Args:
            user_id: Identifier of the user.
            request: Updated user information.

        Returns:
            The updated user.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        user = await self.get_by_user_id(user_id)

        update_data = request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        return await self._repository.update(user)

    async def delete(
        self,
        user_id: UUID,
    ) -> None:
        """
        Soft delete a user.

        Args:
            user_id: Identifier of the user.

        Raises:
            UserNotFoundError: If the user does not exist.
        """
        user = await self.get_by_user_id(user_id)

        await self._repository.delete(user)

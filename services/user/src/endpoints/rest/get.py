"""
Defines the endpoint for retrieving a user.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, status

from ...dependencies.get_user_manager import get_user_manager
from ...managers.interfaces.user import UserManagerProtocol
from ...models.data_validation.user_response import UserResponse
from ...routers.user import router as user_router


@user_router.get(
    path="/{user_id}",
    name="Get User",
    deprecated=False,
    include_in_schema=True,
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: UUID,
    manager: Annotated[UserManagerProtocol, Depends(get_user_manager)]
) -> UserResponse:
    """
    Retrieve an active user by its unique identifier.

    Args:
        user_id: The unique identifier of the user.
        manager: User manager used to retrieve the user.

    Returns:
        The requested user.
    """
    user = await manager.get_by_user_id(user_id)

    return UserResponse.model_validate(user)

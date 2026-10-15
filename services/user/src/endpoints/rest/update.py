"""
Defines the endpoint for updating an existing user.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, status

from ...dependencies.get_user_manager import get_user_manager
from ...managers.interfaces.user import UserManagerProtocol
from ...models.data_validation.user_request_update_base import (
    UserRequestUpdateBase,
)
from ...models.data_validation.user_response import UserResponse
from ...routers.user import router as user_router


@user_router.patch(
    path="/{user_id}",
    name="Update User",
    deprecated=False,
    include_in_schema=True,
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_user(
    user_id: UUID,
    user: UserRequestUpdateBase,
    manager: Annotated[UserManagerProtocol, Depends(get_user_manager)]
) -> UserResponse:
    """
    Update an existing user.

    Args:
        user_id: The unique identifier of the user.
        user: The user update request payload.
        manager: User manager used to perform the update operation.

    Returns:
        The updated user.

    Raises:
        HTTPException: If the user does not exist.
    """
    updated_user = await manager.update(
        user_id=user_id,
        request=user,
    )

    return UserResponse.model_validate(updated_user)

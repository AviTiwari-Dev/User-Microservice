"""
Defines the endpoint for creating a user.
"""

from fastapi import Depends, status

from ...dependencies.get_user_manager import get_user_manager
from ...managers.interfaces.user import UserManagerProtocol
from ...models.data_validation.user_request_base import UserRequestBase
from ...models.data_validation.user_response import UserResponse
from ...routers.user import router as user_router


@user_router.post(
    path="/",
    name="Create User",
    deprecated=False,
    include_in_schema=True,
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_user(
    user: UserRequestBase,
    manager: UserManagerProtocol = Depends(get_user_manager),
) -> UserResponse:
    """
    Create a new user.

    Args:
        user: The user creation request payload.
        manager: User manager used to perform the creation operation.

    Returns:
        The newly created user.
    """
    created_user = await manager.create(user)

    return UserResponse.model_validate(created_user)

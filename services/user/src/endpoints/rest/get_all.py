"""
Defines the endpoint for retrieving a paginated list of users.
"""

from uuid import UUID

from fastapi import Depends, Query, status

from ...dependencies.get_user_manager import get_user_manager
from ...managers.interfaces.user import UserManagerProtocol
from ...models.data_validation.user_response import UserResponse
from ...routers.user import router as user_router


@user_router.get(
    path="/",
    name="Get Users",
    deprecated=False,
    include_in_schema=True,
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    cursor: UUID | None = Query(
        default=None,
        description="Cursor identifying the last user returned by the previous page.",
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
        description="Maximum number of users to return.",
    ),
    manager: UserManagerProtocol = Depends(get_user_manager),
) -> list[UserResponse]:
    """
    Retrieve a paginated list of active users.

    Args:
        cursor: Cursor used to retrieve the next page of users.
        limit: Maximum number of users to return.
        manager: User manager used to retrieve users.

    Returns:
        A paginated list of active users.
    """
    users = await manager.get_all(
        cursor=cursor,
        limit=limit,
    )

    return [UserResponse.model_validate(user) for user in users]

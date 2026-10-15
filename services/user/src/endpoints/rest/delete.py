"""
Defines the endpoint for deleting a user.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Response, status

from ...dependencies.get_user_manager import get_user_manager
from ...managers.interfaces.user import UserManagerProtocol
from ...routers.user import router as user_router


@user_router.delete(
    path="/{user_id}",
    name="Delete User",
    deprecated=False,
    include_in_schema=True,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: UUID,
    manager: Annotated[UserManagerProtocol, Depends(get_user_manager)]
) -> Response:
    """
    Soft delete an existing user.

    Args:
        user_id: The unique identifier of the user.
        manager: User manager used to perform the delete operation.

    Returns:
        An empty response indicating that the user was successfully
        deleted.
    """
    await manager.delete(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

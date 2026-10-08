"""
Defines the Pydantic response model for user resources.
"""

from typing import Annotated
from uuid import UUID

from pydantic import ConfigDict, Field

from .user_request_base import UserRequestBase


class UserResponse(UserRequestBase):
    """
    Represents the response returned for a user resource.

    Extends the base user request model by including the unique
    identifier assigned to the user.
    """

    user_id: Annotated[
        UUID,
        Field(
            title="User ID",
            description="The unique identifier of the user.",
            deprecated=False,
            strict=True,
        ),
    ]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

"""
Defines the base Pydantic model for user request payloads.
"""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ...enums.gender import GenderEnum


class UserRequestBase(BaseModel):
    """
    Base model for user-related API requests.

    Defines the common fields and validation rules for user identity
    information shared across request models, such as creating and
    updating a user.
    """

    first_name: Annotated[
        str,
        Field(
            title="First Name",
            description="The user's first name.",
            deprecated=False,
            min_length=1,
            max_length=25,
            pattern=r"^[a-zA-Z]+$",
            strict=True,
        ),
    ]
    middle_name: Annotated[
        str,
        Field(
            title="Middle Name",
            description="The user's middle name.",
            deprecated=False,
            min_length=0,
            max_length=25,
            pattern=r"^[a-zA-Z]*$",
            strict=True,
        ),
    ]
    last_name: Annotated[
        str,
        Field(
            title="Last Name",
            description="The user's last name.",
            deprecated=False,
            min_length=0,
            max_length=25,
            pattern=r"^[a-zA-Z]*$",
            strict=True,
        ),
    ]
    date_of_birth: Annotated[
        date,
        Field(
            title="Date of Birth",
            description="The user's date of birth.",
            deprecated=False,
            strict=False,
        ),
    ]
    gender: Annotated[
        GenderEnum,
        Field(
            title="Gender",
            description="The user's gender.",
            deprecated=False,
            strict=False,
        ),
    ]

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("first_name", "middle_name", "last_name", mode="after")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        """
        Normalizes a user's name.

        Converts the provided name to lowercase to ensure consistent
        storage and comparisons throughout the application.

        Args:
            value: The name value to normalize.

        Returns:
            The normalized lowercase name.
        """
        return value.lower()

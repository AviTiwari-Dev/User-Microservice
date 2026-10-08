"""
Defines the base Pydantic model for user update request payloads.
"""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ...enums.gender import GenderEnum


class UserRequestUpdateBase(BaseModel):
    """
    Base model for user update API requests.

    Defines the fields and validation rules for updating user identity
    information. All fields are optional to support partial updates.
    """

    first_name: Annotated[
        str | None,
        Field(
            title="First Name",
            description="The user's first name.",
            deprecated=False,
            min_length=1,
            max_length=25,
            pattern=r"^[a-zA-Z]+$",
            strict=True,
        ),
    ] = None

    middle_name: Annotated[
        str | None,
        Field(
            title="Middle Name",
            description="The user's middle name.",
            deprecated=False,
            min_length=0,
            max_length=25,
            pattern=r"^[a-zA-Z]*$",
            strict=True,
        ),
    ] = None

    last_name: Annotated[
        str | None,
        Field(
            title="Last Name",
            description="The user's last name.",
            deprecated=False,
            min_length=0,
            max_length=25,
            pattern=r"^[a-zA-Z]*$",
            strict=True,
        ),
    ] = None

    date_of_birth: Annotated[
        date | None,
        Field(
            title="Date of Birth",
            description="The user's date of birth.",
            deprecated=False,
            strict=False,
        ),
    ] = None

    gender: Annotated[
        GenderEnum | None,
        Field(
            title="Gender",
            description="The user's gender.",
            deprecated=False,
            strict=False,
        ),
    ] = None

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("first_name", "middle_name", "last_name", mode="after")
    @classmethod
    def normalize_full_name(cls, value: str | None) -> str | None:
        """
        Normalizes a user's name.

        Converts the provided name to lowercase when a value is supplied.
        Fields omitted from the request remain unchanged.

        Args:
            value: The name value to normalize.

        Returns:
            The normalized lowercase name, or ``None`` if no value was
            provided.
        """
        return value.lower() if value is not None else None

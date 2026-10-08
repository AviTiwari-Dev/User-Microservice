"""
Defines the SQLAlchemy ORM model for storing user identity information.
"""

from datetime import date, datetime
from uuid import UUID, uuid7

from sqlalchemy import Date, DateTime, Enum, Index, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from ...bases.user import UserBase
from ...enums.gender import GenderEnum


class User(UserBase):
    """
    Represents a user within the identity service.

    Stores personal identity information for a user, including their
    name, date of birth, gender, and audit timestamps.
    """

    __tablename__ = "users"

    #: Unique identifier for the user.
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )

    #: User's first name.
    first_name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )

    #: User's middle name.
    middle_name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )

    #: User's last name.
    last_name: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )

    #: User's date of birth.
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    #: User's gender.
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="genderenum"),
        nullable=False,
    )

    #: Timestamp indicating when the user record was created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    #: Timestamp indicating when the user record was last updated.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    #: Timestamp indicating when the user record was soft deleted.
    #: A value of ``None`` indicates that the record is active.
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    __table_args__ = (
        #: Partial index with user_id and deleted_at column(created at end of file after declaration of columns)
        Index(
            "ix_users_active",
            "user_id",
            postgresql_where=deleted_at.is_(None),
        ),
        {"schema": "user_schema"},
    )

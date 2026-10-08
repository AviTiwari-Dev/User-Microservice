"""
Defines the SQLAlchemy declarative base class for the identity module.
"""

from sqlalchemy.orm import DeclarativeBase


class UserBase(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models in the identity module.

    Provides the shared declarative metadata used to define database
    tables and ORM mappings for identity-related entities, including
    user profiles and personal information managed by the identity
    service.
    """

    pass

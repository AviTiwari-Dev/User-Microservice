"""
Creates the SQLAlchemy asynchronous session factory used throughout the application.

The session factory is responsible for creating ``AsyncSession`` instances
that manage database transactions and interactions with the configured
database engine.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..engines.user import engine as user_engine

# Create the application's asynchronous session factory.
#
# Parameters:
# - bind: SQLAlchemy engine used to establish database connections.
# - class_: Session class to instantiate for each database session.
# - expire_on_commit: Prevents ORM objects from being expired after a
#   successful transaction commit, allowing attribute access without
#   reloading them from the database.
# - autoflush: Automatically synchronizes pending changes with the database
#   before executing queries that depend on those changes.
session_factory = async_sessionmaker(
    bind=user_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
)

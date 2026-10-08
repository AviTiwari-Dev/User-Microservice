import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from tests.configurations.env_variables.test import get_test_configurations

from services.user.src.bases.user import UserBase
from services.user.src.repositories.implementation.postgresql.user import (
    PostgresqlUserRepository,
)

test_configuration_variables = get_test_configurations()


@pytest_asyncio.fixture
async def repository(session: AsyncSession):
    return PostgresqlUserRepository(session)


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    engine = create_async_engine(
        test_configuration_variables.TEST_URL,
        echo=False,
    )

    async with engine.begin() as connection:
        await connection.exec_driver_sql(
            "CREATE SCHEMA IF NOT EXISTS user_schema"
        )
        await connection.run_sync(UserBase.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(UserBase.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with SessionLocal() as session:
        yield session

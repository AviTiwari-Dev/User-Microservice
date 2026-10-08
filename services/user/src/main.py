"""
User microservice
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from . import endpoints  # noqa: F401
from .bases.user import UserBase

# from .configurations.databases.seed import seed as seed_database
from .configurations.env_variables.user_api import get_user_api_configuration
from .engines.user import engine as user_engine
from .exception_handlers.register import register_exception_handlers
from .routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage User API application startup and shutdown.

    During startup, the User API database schema and tables are created
    if they do not already exist. Application resources can also be
    initialized here.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control to the running FastAPI application.

    Note:
        Database schema management should eventually be handled by
        Alembic migrations rather than ``metadata.create_all()`` in
        production environments.
    """

    async with user_engine.begin() as connection:
        # Create schemas
        await connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS user_schema")
        )

        # Create tables
        await connection.run_sync(UserBase.metadata.create_all)

    # Seed initial data
    # await seed_database()

    yield


user_api_configuration_variables = get_user_api_configuration()

user_api = FastAPI(
    title="User API's",
    version=user_api_configuration_variables.APP_VERSION,
    debug=user_api_configuration_variables.ENVIRONMENT != "production",
    deprecated=False,
    include_in_schema=True,
    description="User api's microservice.",
    summary="User api's microservice.",
    lifespan=lifespan,
    docs_url="/documentation/Swagger",
    redoc_url="/documentation/ReDoc",
    openapi_url="/documentation/openapi.json",
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
    contact={
        "name": "Avi Tiwari",
        "email": "email@example.com",
    },
)

# Add routers
user_api.include_router(
    user_router,
    prefix=f"/api/v{user_api_configuration_variables.API_VERSION}",
)

# Add exception handlers
register_exception_handlers(user_api)

"""
Creates and configures the application's asynchronous SQLAlchemy engine.

The engine manages database connections and connection pooling for all
asynchronous database operations performed by the application.
"""

from sqlalchemy.ext.asyncio import create_async_engine

from ..configurations.env_variables.engine import get_engine_configuration

# Create the application's asynchronous SQLAlchemy engine.
#
# Parameters:
# - url: Database connection URL.
# - echo: Enables SQL statement logging when set to True.
# - pool_size: Number of persistent connections maintained in the pool.
# - max_overflow: Maximum number of temporary connections allowed beyond
#   the configured pool size.
# - pool_timeout: Maximum time (in seconds) to wait for an available
#   connection before raising an exception.
# - pool_recycle: Maximum lifetime (in seconds) of a pooled connection
#   before it is recycled.
# - future: Enables SQLAlchemy 2.x style behavior.
# - connect_args: Additional driver-specific connection arguments.
#   Here, PostgreSQL JIT compilation is disabled to reduce overhead for
#   short-lived queries.

engine_configuration_variables = get_engine_configuration()

engine = create_async_engine(
    url=engine_configuration_variables.URL,
    echo=engine_configuration_variables.ECHO,
    pool_size=engine_configuration_variables.POOL_SIZE,
    max_overflow=engine_configuration_variables.MAX_OVERFLOW,
    pool_timeout=engine_configuration_variables.POOL_TIMEOUT,
    pool_recycle=engine_configuration_variables.POOL_RECYCLE,
    future=engine_configuration_variables.FUTURE,
    connect_args={
        "server_settings": {
            "jit": "off",
        }
    },
)

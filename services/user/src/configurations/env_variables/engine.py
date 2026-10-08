"""
Loads and validates database engine configuration from environment variables.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """
    Database engine configuration.

    Attributes:
        URL: SQLAlchemy database connection URL.
        ECHO: Enables SQL statement logging when set to ``True``.
        POOL_SIZE: Number of persistent connections maintained in the
            connection pool.
        MAX_OVERFLOW: Maximum number of temporary connections allowed
            beyond the configured pool size.
        POOL_TIMEOUT: Maximum time, in seconds, to wait for an available
            connection before raising an exception.
        POOL_RECYCLE: Maximum lifetime, in seconds, of a pooled connection
            before it is recycled.
        FUTURE: Enables SQLAlchemy 2.x style behavior.
    """

    URL: str
    ECHO: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_TIMEOUT: int
    POOL_RECYCLE: int
    FUTURE: bool

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


@lru_cache
def get_engine_configuration() -> Settings:
    """
    Return the cached database engine configuration.

    The settings object is created only on the first invocation and
    reused for subsequent calls within the application process.

    Returns:
        The application database engine configuration.
    """
    return Settings()  # pyright: ignore[reportCallIssue]

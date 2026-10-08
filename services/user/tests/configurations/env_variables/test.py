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
        TEST_URL: SQLAlchemy test database connection URL.
    """

    TEST_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


@lru_cache
def get_test_configurations() -> Settings:
    """
    Return the cached test configuration.

    The settings object is created only on the first invocation
    and reused for subsequent calls within the test process.

    Returns:
        The test configuration settings.
    """
    return Settings()  # pyright: ignore[reportCallIssue]

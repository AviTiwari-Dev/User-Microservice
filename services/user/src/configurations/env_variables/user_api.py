"""
Auth API configuration variables
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """ """

    ENVIRONMENT: str
    APP_VERSION: str
    API_VERSION: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


@lru_cache
def get_user_api_configuration() -> Settings:
    """
    Return the cached User API configuration.

    The ``Settings`` instance is created only on the first invocation
    and reused for subsequent calls within the application process.

    Returns:
        The User API application configuration.
    """
    return Settings()  # pyright: ignore[reportCallIssue]

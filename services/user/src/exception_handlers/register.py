from fastapi import FastAPI

from ..exceptions.user_not_found_error import UserNotFoundError
from .handlers import not_found_handler


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register application exception handlers.

    Args:
        app: FastAPI application.
    """
    app.add_exception_handler(
        UserNotFoundError,
        not_found_handler,
    )

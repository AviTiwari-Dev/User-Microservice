"""HTTP exception handlers for the User API."""

import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def unauthorized_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unauthorized access exceptions.

    Args:
        request: The incoming HTTP request.
        exc: The exception raised during request processing.

    Returns:
        A JSON response with HTTP 401 status and the exception detail.
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": str(exc),
        },
    )


async def forbidden_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle forbidden access exceptions.

    Args:
        request: The incoming HTTP request.
        exc: The exception raised during request processing.

    Returns:
        A JSON response with HTTP 403 status and the exception detail.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": str(exc),
        },
    )


async def not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle resource-not-found exceptions.

    Args:
        request: The incoming HTTP request.
        exc: The exception raised during request processing.

    Returns:
        A JSON response with HTTP 404 status and the exception detail.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


async def conflict_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle resource-conflict exceptions.

    Args:
        request: The incoming HTTP request.
        exc: The exception raised during request processing.

    Returns:
        A JSON response with HTTP 409 status and the exception detail.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
        },
    )


async def internal_server_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected internal server errors.

    The actual exception is logged for server-side diagnostics, while
    a generic error message is returned to the client to avoid exposing
    internal implementation details.

    Args:
        request: The incoming HTTP request.
        exc: The unexpected exception raised during request processing.

    Returns:
        A JSON response with HTTP 500 status and a generic error message.
    """
    logger.exception(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
        },
    )

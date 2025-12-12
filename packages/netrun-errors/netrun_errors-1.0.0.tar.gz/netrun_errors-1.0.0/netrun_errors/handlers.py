"""
Global exception handlers for FastAPI applications.

Provides centralized exception handling with structured JSON responses,
correlation ID injection, and logging integration.
"""

import logging
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .base import NetrunException

logger = logging.getLogger(__name__)


async def netrun_exception_handler(
    request: Request, exc: NetrunException
) -> JSONResponse:
    """
    Handle NetrunException instances with structured JSON responses.

    Args:
        request: FastAPI request object
        exc: NetrunException instance

    Returns:
        JSONResponse with structured error format
    """
    # Add request path to error details
    error_dict = exc.to_dict()
    error_dict["error"]["path"] = str(request.url.path)

    # Log error with correlation ID
    logger.error(
        f"NetrunException: {exc.error_code} - {exc.message}",
        extra={
            "correlation_id": exc.correlation_id,
            "error_code": exc.error_code,
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_dict,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle FastAPI request validation errors with structured format.

    Args:
        request: FastAPI request object
        exc: RequestValidationError instance

    Returns:
        JSONResponse with validation error details
    """
    from datetime import datetime, timezone

    correlation_id = NetrunException._generate_correlation_id()

    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": {
                "validation_errors": exc.errors(),
            },
            "correlation_id": correlation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
        }
    }

    logger.warning(
        f"Validation error: {request.method} {request.url.path}",
        extra={
            "correlation_id": correlation_id,
            "validation_errors": exc.errors(),
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response,
    )


async def http_exception_handler(
    request: Request, exc: Union[StarletteHTTPException, Exception]
) -> JSONResponse:
    """
    Handle generic HTTP exceptions with structured format.

    Args:
        request: FastAPI request object
        exc: HTTPException or generic Exception

    Returns:
        JSONResponse with structured error format
    """
    from datetime import datetime, timezone

    correlation_id = NetrunException._generate_correlation_id()

    # Determine status code
    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "An unexpected error occurred"

    error_response = {
        "error": {
            "code": "HTTP_ERROR",
            "message": message,
            "details": {},
            "correlation_id": correlation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
        }
    }

    logger.error(
        f"HTTP exception: {status_code} - {message}",
        extra={
            "correlation_id": correlation_id,
            "status_code": status_code,
            "path": request.url.path,
            "method": request.method,
        },
        exc_info=True if status_code >= 500 else False,
    )

    return JSONResponse(
        status_code=status_code,
        content=error_response,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unhandled exceptions with structured format.

    Args:
        request: FastAPI request object
        exc: Exception instance

    Returns:
        JSONResponse with generic error format
    """
    from datetime import datetime, timezone

    correlation_id = NetrunException._generate_correlation_id()

    error_response = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "details": {},
            "correlation_id": correlation_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
        }
    }

    logger.exception(
        f"Unhandled exception: {type(exc).__name__}",
        extra={
            "correlation_id": correlation_id,
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response,
    )


def install_exception_handlers(app: FastAPI) -> None:
    """
    Install all Netrun exception handlers on a FastAPI application.

    Usage:
        from fastapi import FastAPI
        from netrun_errors import install_exception_handlers

        app = FastAPI()
        install_exception_handlers(app)

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(NetrunException, netrun_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    logger.info("Netrun exception handlers installed successfully")

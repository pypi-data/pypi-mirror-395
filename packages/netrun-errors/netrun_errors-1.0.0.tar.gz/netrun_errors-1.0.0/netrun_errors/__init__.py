"""
Netrun Unified Error Handling Package.

A comprehensive error handling library for FastAPI applications with:
- Structured JSON error responses
- Automatic correlation ID generation
- Machine-readable error codes
- Global exception handlers
- Request/response logging middleware

Version: 1.0.0
Author: Netrun Systems
License: MIT
"""

__version__ = "1.0.0"

# Base exception
from .base import NetrunException

# Authentication exceptions
from .auth import (
    AuthenticationRequiredError,
    InvalidCredentialsError,
    TokenExpiredError,
    TokenInvalidError,
    TokenRevokedError,
)

# Authorization exceptions
from .authorization import InsufficientPermissionsError, TenantAccessDeniedError

# Resource exceptions
from .resource import ResourceConflictError, ResourceNotFoundError

# Service exceptions
from .service import ServiceUnavailableError, TemporalUnavailableError

# Exception handlers
from .handlers import install_exception_handlers

# Middleware
from .middleware import install_error_logging_middleware

__all__ = [
    # Base
    "NetrunException",
    # Authentication
    "InvalidCredentialsError",
    "TokenExpiredError",
    "TokenInvalidError",
    "TokenRevokedError",
    "AuthenticationRequiredError",
    # Authorization
    "InsufficientPermissionsError",
    "TenantAccessDeniedError",
    # Resource
    "ResourceNotFoundError",
    "ResourceConflictError",
    # Service
    "ServiceUnavailableError",
    "TemporalUnavailableError",
    # Handlers
    "install_exception_handlers",
    # Middleware
    "install_error_logging_middleware",
]

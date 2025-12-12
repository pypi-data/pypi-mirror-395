"""
Service-related exceptions for Netrun Systems.

Exceptions for service availability, external dependencies,
and system-level errors.
"""

from typing import Any, Dict, Optional

from fastapi import status

from .base import NetrunException


class ServiceUnavailableError(NetrunException):
    """
    Raised when service or dependency is temporarily unavailable.

    Common scenarios:
    - Database connection failures
    - External API timeouts
    - Maintenance mode
    - Circuit breaker open

    Status Code: 503 Service Unavailable
    Error Code: SERVICE_UNAVAILABLE
    """

    def __init__(
        self,
        message: str = "Service is temporarily unavailable. Please try again later.",
        details: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            message=message,
            details=details,
            correlation_id=correlation_id,
        )


class TemporalUnavailableError(NetrunException):
    """
    Raised when Temporal workflow engine is unavailable.

    Specific to Netrun Systems' Temporal.io integration for
    long-running workflows and distributed transactions.

    Status Code: 503 Service Unavailable
    Error Code: TEMPORAL_UNAVAILABLE
    """

    def __init__(
        self,
        message: str = "Workflow engine is temporarily unavailable. Please try again later.",
        details: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="TEMPORAL_UNAVAILABLE",
            message=message,
            details=details,
            correlation_id=correlation_id,
        )

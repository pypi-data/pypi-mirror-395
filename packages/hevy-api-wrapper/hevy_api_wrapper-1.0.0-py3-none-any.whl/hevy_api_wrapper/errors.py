"""Exception classes for Hevy API errors."""

from __future__ import annotations

from typing import Any, Optional


class HevyApiError(Exception):
    """Base exception for all Hevy API errors.

    Attributes:
        status_code: HTTP status code of the error response.
        error_code: API-specific error code if provided.
        details: Additional error details from the API response.
        request_id: Unique request identifier for debugging.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        self.request_id = request_id


class AuthError(HevyApiError):
    """Authentication or authorization error (401, 403)."""

    pass


class NotFoundError(HevyApiError):
    """Resource not found error (404)."""

    pass


class RateLimitError(HevyApiError):
    """Rate limit exceeded error (429)."""

    pass


class ServerError(HevyApiError):
    """Server error from the API (5xx)."""

    pass


class ValidationError(HevyApiError):
    """Request validation error (400)."""

    pass


def raise_for_status(
    *,
    status_code: int,
    message: str,
    error_code: Optional[str] = None,
    details: Optional[Any] = None,
    request_id: Optional[str] = None,
) -> None:
    """Raise appropriate exception based on HTTP status code.

    Args:
        status_code: HTTP status code from the response.
        message: Error message to include in the exception.
        error_code: Optional API-specific error code.
        details: Optional additional error details.
        request_id: Optional request identifier for debugging.

    Raises:
        ValidationError: For 400 status codes.
        AuthError: For 401 and 403 status codes.
        NotFoundError: For 404 status codes.
        RateLimitError: For 429 status codes.
        ServerError: For 5xx status codes.
        HevyApiError: For any other error status codes.
    """
    if 200 <= status_code < 300:
        return
    if status_code == 400:
        raise ValidationError(
            message,
            status_code=status_code,
            error_code=error_code,
            details=details,
            request_id=request_id,
        )
    if status_code in (401, 403):
        raise AuthError(
            message,
            status_code=status_code,
            error_code=error_code,
            details=details,
            request_id=request_id,
        )
    if status_code == 404:
        raise NotFoundError(
            message,
            status_code=status_code,
            error_code=error_code,
            details=details,
            request_id=request_id,
        )
    if status_code == 429:
        raise RateLimitError(
            message,
            status_code=status_code,
            error_code=error_code,
            details=details,
            request_id=request_id,
        )
    if 500 <= status_code < 600:
        raise ServerError(
            message,
            status_code=status_code,
            error_code=error_code,
            details=details,
            request_id=request_id,
        )
    raise HevyApiError(
        message,
        status_code=status_code,
        error_code=error_code,
        details=details,
        request_id=request_id,
    )

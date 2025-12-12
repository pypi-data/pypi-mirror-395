"""Hevy API Wrapper - Python client for the Hevy fitness tracking API.

This package provides both synchronous and asynchronous clients for interacting
with the Hevy API, complete with type-safe models and comprehensive error handling.
"""

from .client import AsyncClient, Client
from .errors import (
    AuthError,
    HevyApiError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .version import __version__

__all__ = [
    "Client",
    "AsyncClient",
    "__version__",
    "HevyApiError",
    "AuthError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
]

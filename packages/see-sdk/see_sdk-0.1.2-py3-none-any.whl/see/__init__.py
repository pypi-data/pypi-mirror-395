"""
SEE - A modern Python SDK for SEE services.

This package provides a clean and type-safe interface for interacting
with SEE services.
"""

from .client import SeeClient
from .exceptions import (
    SeeError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError,
)

__version__ = "0.1.0"
__all__ = [
    "SeeClient",
    "SeeError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
]

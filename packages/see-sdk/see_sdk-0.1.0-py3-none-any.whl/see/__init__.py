"""
SEE URL - A modern Python SDK for URL shortening service.

This package provides a clean and type-safe interface for interacting
with URL shortening services.
"""

from .client import SeeClient
from .exceptions import (
    SeeUrlError,
    APIError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError,
)

__version__ = "0.1.0"
__all__ = [
    "SeeClient",
    "SeeUrlError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "NotFoundError",
]

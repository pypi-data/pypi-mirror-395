"""Custom exceptions for SEE SDK."""

from typing import Any


class SeeError(Exception):
    """Base exception for all SEE SDK errors."""

    def __init__(self, message: str, *args: Any) -> None:
        super().__init__(message, *args)
        self.message = message


class APIError(SeeError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(APIError):
    """Raised when authentication fails."""

    pass


class ValidationError(SeeError):
    """Raised when input validation fails."""

    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class NotFoundError(APIError):
    """Raised when a resource is not found."""

    pass

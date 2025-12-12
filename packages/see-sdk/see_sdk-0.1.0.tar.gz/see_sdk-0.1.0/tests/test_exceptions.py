"""Tests for exception classes."""

import pytest

from see.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    SeeUrlError,
    ValidationError,
)


def test_see_url_error() -> None:
    """Test base SeeUrlError exception."""
    error = SeeUrlError("Test error")
    assert str(error) == "Test error"
    assert error.message == "Test error"


def test_api_error() -> None:
    """Test APIError exception with status code and response data."""
    error = APIError(
        message="API failed",
        status_code=500,
        response_data={"error": "Internal server error"},
    )
    assert error.message == "API failed"
    assert error.status_code == 500
    assert error.response_data == {"error": "Internal server error"}


def test_api_error_without_optional_params() -> None:
    """Test APIError without optional parameters."""
    error = APIError("Simple error")
    assert error.message == "Simple error"
    assert error.status_code is None
    assert error.response_data == {}


def test_authentication_error() -> None:
    """Test AuthenticationError is subclass of APIError."""
    error = AuthenticationError("Auth failed", status_code=401)
    assert isinstance(error, APIError)
    assert error.message == "Auth failed"
    assert error.status_code == 401


def test_validation_error() -> None:
    """Test ValidationError exception."""
    error = ValidationError("Invalid input")
    assert isinstance(error, SeeUrlError)
    assert error.message == "Invalid input"


def test_rate_limit_error() -> None:
    """Test RateLimitError with retry_after."""
    error = RateLimitError(retry_after=60, status_code=429)
    assert isinstance(error, APIError)
    assert error.retry_after == 60
    assert error.status_code == 429


def test_rate_limit_error_default_message() -> None:
    """Test RateLimitError with default message."""
    error = RateLimitError()
    assert error.message == "Rate limit exceeded"
    assert error.retry_after is None


def test_not_found_error() -> None:
    """Test NotFoundError exception."""
    error = NotFoundError("Resource not found", status_code=404)
    assert isinstance(error, APIError)
    assert error.message == "Resource not found"
    assert error.status_code == 404

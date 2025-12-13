"""Tests for error handling."""

from legnext.types.errors import (
    AuthenticationError,
    Error,
    LegnextAPIError,
    NotFoundError,
    RateLimitError,
)


def test_error_model():
    """Test Error model."""
    error = Error(code=400, message="Bad request", detail={"field": "invalid"})
    assert error.code == 400
    assert error.message == "Bad request"
    assert error.detail["field"] == "invalid"


def test_legnext_api_error():
    """Test LegnextAPIError."""
    error = Error(code=400, message="Bad request")
    exc = LegnextAPIError("Request failed", 400, error)

    assert exc.message == "Request failed"
    assert exc.status_code == 400
    assert exc.error == error
    assert str(exc) == "Request failed"


def test_authentication_error():
    """Test AuthenticationError."""
    error = Error(code=401, message="Unauthorized")
    exc = AuthenticationError("Invalid API key", 401, error)

    assert exc.status_code == 401
    assert isinstance(exc, LegnextAPIError)


def test_rate_limit_error():
    """Test RateLimitError."""
    error = Error(code=429, message="Rate limit exceeded")
    exc = RateLimitError("Too many requests", 429, error)

    assert exc.status_code == 429
    assert isinstance(exc, LegnextAPIError)


def test_not_found_error():
    """Test NotFoundError."""
    error = Error(code=404, message="Job not found")
    exc = NotFoundError("Resource not found", 404, error)

    assert exc.status_code == 404
    assert isinstance(exc, LegnextAPIError)

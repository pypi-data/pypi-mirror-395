"""Error types for the Legnext SDK."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class Error(BaseModel):
    """API error details."""

    code: int = Field(description="Error code")
    message: str = Field(description="Human-readable error message")
    raw_message: Optional[str] = Field(None, description="Raw error message from service")
    detail: Optional[dict[str, Any]] = Field(None, description="Additional error details")

    model_config = ConfigDict(populate_by_name=True)


class LegnextError(Exception):
    """Base exception for all Legnext SDK errors."""

    def __init__(self, message: str, error: Optional[Error] = None) -> None:
        self.message = message
        self.error = error
        super().__init__(message)


class LegnextAPIError(LegnextError):
    """Exception raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int,
        error: Optional[Error] = None,
        response_body: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(LegnextAPIError):
    """Exception raised for authentication failures (401)."""

    pass


class RateLimitError(LegnextAPIError):
    """Exception raised when rate limit is exceeded (429)."""

    pass


class ValidationError(LegnextAPIError):
    """Exception raised for invalid request parameters (400)."""

    pass


class NotFoundError(LegnextAPIError):
    """Exception raised when resource is not found (404)."""

    pass


class ServerError(LegnextAPIError):
    """Exception raised for server errors (500+)."""

    pass


class TimeoutError(LegnextError):
    """Exception raised when a request times out."""

    pass


class ConnectionError(LegnextError):
    """Exception raised when connection fails."""

    pass

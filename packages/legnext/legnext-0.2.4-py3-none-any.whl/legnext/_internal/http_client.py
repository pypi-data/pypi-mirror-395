"""HTTP client implementation for the Legnext SDK."""

import time
from typing import Any, Dict, Literal, Optional, cast

import httpx

from legnext.types.errors import (
    AuthenticationError,
    ConnectionError,
    Error,
    LegnextAPIError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


class BaseHTTPClient:
    """Base HTTP client with common functionality."""

    DEFAULT_BASE_URL = "https://api.legnext.ai/api"
    DEFAULT_TIMEOUT = 60.0
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for API requests (defaults to production URL)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            custom_headers: Additional headers to include in requests
        """
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.custom_headers = custom_headers or {}

    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for requests."""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "legnext-python/0.2.4",
        }
        headers.update(self.custom_headers)
        return headers

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Determine if a request should be retried.

        Args:
            status_code: HTTP status code
            attempt: Current retry attempt number

        Returns:
            True if the request should be retried
        """
        if attempt >= self.max_retries:
            return False

        # Retry on rate limits and server errors
        return status_code in (429, 500, 502, 503, 504)

    def _get_retry_delay(self, attempt: int, retry_after: Optional[str] = None) -> float:
        """Calculate delay before retry.

        Args:
            attempt: Current retry attempt number
            retry_after: Value from Retry-After header if present

        Returns:
            Delay in seconds
        """
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass

        # Exponential backoff: 1s, 2s, 4s, etc.
        return float(min(2**attempt, 30))

    def _parse_error(self, response: httpx.Response) -> Error:
        """Parse error from response.

        Args:
            response: HTTP response

        Returns:
            Parsed error object
        """
        try:
            data = response.json()
            if "error" in data:
                error_data = data["error"]
                return Error(
                    code=error_data.get("code", response.status_code),
                    message=error_data.get("message", "Unknown error"),
                    raw_message=error_data.get("raw_message"),
                    detail=error_data.get("detail"),
                )
        except Exception:
            pass

        return Error(
            code=response.status_code,
            message=f"HTTP {response.status_code}: {response.reason_phrase}",
        )

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Raise appropriate exception for error responses.

        Args:
            response: HTTP response

        Raises:
            LegnextAPIError: For API errors
        """
        if response.is_success:
            return

        error = self._parse_error(response)
        status_code = response.status_code

        try:
            response_body = response.json()
        except Exception:
            response_body = None

        error_message = error.message

        if status_code == 401:
            raise AuthenticationError(error_message, status_code, error, response_body)
        elif status_code == 404:
            raise NotFoundError(error_message, status_code, error, response_body)
        elif status_code == 429:
            raise RateLimitError(error_message, status_code, error, response_body)
        elif status_code == 400:
            raise ValidationError(error_message, status_code, error, response_body)
        elif status_code >= 500:
            raise ServerError(error_message, status_code, error, response_body)
        else:
            raise LegnextAPIError(error_message, status_code, error, response_body)


class HTTPClient(BaseHTTPClient):
    """Synchronous HTTP client."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = BaseHTTPClient.DEFAULT_TIMEOUT,
        max_retries: int = BaseHTTPClient.DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the synchronous HTTP client."""
        super().__init__(api_key, base_url, timeout, max_retries, custom_headers)
        self._client: Optional[httpx.Client] = None

    def __enter__(self) -> "HTTPClient":
        """Context manager entry."""
        self._client = httpx.Client(timeout=self.timeout)
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.Client(timeout=self.timeout)
        return self._client

    def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response JSON data

        Raises:
            LegnextAPIError: For API errors
            ConnectionError: For connection errors
            TimeoutError: For timeout errors
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = self._get_headers()

        # Remove Content-Type for multipart requests
        if files:
            headers.pop("Content-Type", None)

        client = self._get_client()
        attempt = 0

        while True:
            try:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                )

                # Check if we should retry
                if self._should_retry(response.status_code, attempt):
                    retry_after = response.headers.get("Retry-After")
                    delay = self._get_retry_delay(attempt, retry_after)
                    time.sleep(delay)
                    attempt += 1
                    continue

                # Raise for error status codes
                self._raise_for_status(response)

                # Return JSON response
                return cast(Dict[str, Any], response.json())

            except httpx.TimeoutException as e:
                if attempt >= self.max_retries:
                    raise TimeoutError(f"Request timed out after {self.timeout}s") from e
                attempt += 1
                time.sleep(self._get_retry_delay(attempt))

            except httpx.ConnectError as e:
                if attempt >= self.max_retries:
                    raise ConnectionError(f"Failed to connect to {url}") from e
                attempt += 1
                time.sleep(self._get_retry_delay(attempt))


class AsyncHTTPClient(BaseHTTPClient):
    """Asynchronous HTTP client."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = BaseHTTPClient.DEFAULT_TIMEOUT,
        max_retries: int = BaseHTTPClient.DEFAULT_MAX_RETRIES,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the asynchronous HTTP client."""
        super().__init__(api_key, base_url, timeout, max_retries, custom_headers)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncHTTPClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.aclose()

    async def aclose(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def request(
        self,
        method: HttpMethod,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an async HTTP request.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload

        Returns:
            Response JSON data

        Raises:
            LegnextAPIError: For API errors
            ConnectionError: For connection errors
            TimeoutError: For timeout errors
        """
        import asyncio

        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = self._get_headers()

        # Remove Content-Type for multipart requests
        if files:
            headers.pop("Content-Type", None)

        client = self._get_client()
        attempt = 0

        while True:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                )

                # Check if we should retry
                if self._should_retry(response.status_code, attempt):
                    retry_after = response.headers.get("Retry-After")
                    delay = self._get_retry_delay(attempt, retry_after)
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue

                # Raise for error status codes
                self._raise_for_status(response)

                # Return JSON response
                return cast(Dict[str, Any], response.json())

            except httpx.TimeoutException as e:
                if attempt >= self.max_retries:
                    raise TimeoutError(f"Request timed out after {self.timeout}s") from e
                attempt += 1
                await asyncio.sleep(self._get_retry_delay(attempt))

            except httpx.ConnectError as e:
                if attempt >= self.max_retries:
                    raise ConnectionError(f"Failed to connect to {url}") from e
                attempt += 1
                await asyncio.sleep(self._get_retry_delay(attempt))

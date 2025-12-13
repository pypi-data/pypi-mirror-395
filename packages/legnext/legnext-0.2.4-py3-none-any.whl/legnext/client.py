"""Main client classes for the Legnext SDK."""

from types import TracebackType
from typing import Optional, Type

from legnext._internal.http_client import AsyncHTTPClient, HTTPClient
from legnext.resources.account import AccountResource, AsyncAccountResource
from legnext.resources.midjourney import AsyncMidjourneyResource, MidjourneyResource
from legnext.resources.tasks import AsyncTasksResource, TasksResource


class Client:
    """Synchronous client for the Legnext API.

    Example:
        ```python
        from legnext import Client

        client = Client(api_key="your-api-key")

        # Generate an image
        response = client.midjourney.diffusion(text="a beautiful sunset")
        print(response.job_id)

        # Wait for completion
        result = client.tasks.wait_for_completion(response.job_id)
        print(result.output.image_urls)
        ```
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the Legnext client.

        Args:
            api_key: Your Legnext API key
            base_url: Base URL for API requests (defaults to production URL)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self._http = HTTPClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize resources
        self.account = AccountResource(self._http)
        self.midjourney = MidjourneyResource(self._http)
        self.tasks = TasksResource(self._http)

    def __enter__(self) -> "Client":
        """Context manager entry."""
        self._http.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit."""
        self._http.__exit__(exc_type, exc_val, exc_tb)

    def close(self) -> None:
        """Close the client and release resources."""
        self._http.close()


class AsyncClient:
    """Asynchronous client for the Legnext API.

    Example:
        ```python
        import asyncio
        from legnext import AsyncClient

        async def main():
            async with AsyncClient(api_key="your-api-key") as client:
                response = await client.midjourney.diffusion(text="a futuristic city")
                result = await client.tasks.wait_for_completion(response.job_id)
                print(result.output.image_urls)

        asyncio.run(main())
        ```
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the async Legnext client.

        Args:
            api_key: Your Legnext API key
            base_url: Base URL for API requests (defaults to production URL)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self._http = AsyncHTTPClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize resources
        self.account = AsyncAccountResource(self._http)
        self.midjourney = AsyncMidjourneyResource(self._http)
        self.tasks = AsyncTasksResource(self._http)

    async def __aenter__(self) -> "AsyncClient":
        """Async context manager entry."""
        await self._http.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Async context manager exit."""
        await self._http.__aexit__(exc_type, exc_val, exc_tb)

    async def aclose(self) -> None:
        """Close the client and release resources."""
        await self._http.aclose()

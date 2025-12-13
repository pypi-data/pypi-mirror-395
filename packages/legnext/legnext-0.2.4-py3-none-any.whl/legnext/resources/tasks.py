"""Task management resources."""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from legnext._internal.http_client import AsyncHTTPClient, HTTPClient
from legnext.types.enums import JobStatus
from legnext.types.errors import LegnextAPIError, TimeoutError
from legnext.types.responses import TaskResponse


class BaseTasksResource(ABC):
    """Base class for task management resources.

    Implements common business logic for both sync and async versions.
    Subclasses only need to implement the request and sleep methods.
    """

    def _validate_task_response(self, task: TaskResponse) -> Optional[TaskResponse]:
        """Check if task is complete or failed.

        Returns:
            The task if complete, None if still processing

        Raises:
            LegnextAPIError: If task failed
        """
        if task.status == JobStatus.COMPLETED:
            return task

        if task.status == JobStatus.FAILED:
            error_msg = task.error.message if task.error else "Task failed"
            raise LegnextAPIError(error_msg, 500, task.error)

        return None

    def _parse_task_response(self, data: Dict[str, Any]) -> TaskResponse:
        """Parse API response into TaskResponse."""
        return TaskResponse.model_validate(data)

    @abstractmethod
    async def _fetch_task(self, job_id: str) -> TaskResponse:
        """Fetch task status. Must be implemented by subclasses."""
        pass

    @abstractmethod
    async def _sleep(self, duration: float) -> None:
        """Sleep for duration. Must be implemented by subclasses."""
        pass

    async def _wait_for_completion_impl(
        self,
        job_id: str,
        timeout: float,
        poll_interval: float,
        on_progress: Optional[Callable[[TaskResponse], None]],
    ) -> TaskResponse:
        """Implementation of wait_for_completion (works for both sync and async)."""
        start_time = time.time()

        while True:
            task = await self._fetch_task(job_id)

            if on_progress:
                on_progress(task)

            # Check if task is complete or failed
            result = self._validate_task_response(task)
            if result is not None:
                return result

            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise TimeoutError(f"Task {job_id} did not complete within {timeout} seconds")

            # Wait before retrying
            await self._sleep(poll_interval)


class TasksResource(BaseTasksResource):
    """Synchronous task management resource."""

    def __init__(self, http: HTTPClient) -> None:
        """Initialize the tasks resource."""
        self._http = http

    def get(self, job_id: str) -> TaskResponse:
        """Get the status and results of a task.

        Args:
            job_id: The unique identifier of the job

        Returns:
            Task response with current status and results

        Example:
            ```python
            task = client.tasks.get("job-id-here")
            print(f"Status: {task.status}")
            if task.status == JobStatus.COMPLETED:
                print(f"Results: {task.output}")
            ```
        """
        data = self._http.request("GET", f"/v1/job/{job_id}")
        return self._parse_task_response(data)

    async def _fetch_task(self, job_id: str) -> TaskResponse:
        """Fetch task (sync wrapper)."""
        return self.get(job_id)

    async def _sleep(self, duration: float) -> None:
        """Sleep (sync wrapper)."""
        time.sleep(duration)

    def wait_for_completion(
        self,
        job_id: str,
        *,
        timeout: float = 300.0,
        poll_interval: float = 3.0,
        on_progress: Optional[Callable[[TaskResponse], None]] = None,
    ) -> TaskResponse:
        """Wait for a task to complete.

        Args:
            job_id: The job ID to wait for
            timeout: Maximum time to wait in seconds (default: 300)
            poll_interval: Time between status checks in seconds (default: 3)
            on_progress: Optional callback called on each status check

        Returns:
            Completed task response

        Raises:
            TimeoutError: If task doesn't complete within timeout
            LegnextAPIError: If task fails

        Example:
            ```python
            def print_progress(task):
                print(f"Status: {task.status}")

            result = client.tasks.wait_for_completion(
                job_id="job-id",
                on_progress=print_progress
            )
            print(f"Completed: {result.output.image_urls}")
            ```
        """
        import asyncio

        # Run the async implementation in a sync context
        return asyncio.run(
            self._wait_for_completion_impl(job_id, timeout, poll_interval, on_progress)
        )


class AsyncTasksResource(BaseTasksResource):
    """Asynchronous task management resource."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        """Initialize the async tasks resource."""
        self._http = http

    async def get(self, job_id: str) -> TaskResponse:
        """Get the status and results of a task (async).

        Args:
            job_id: The unique identifier of the job

        Returns:
            Task response with current status and results
        """
        data = await self._http.request("GET", f"/v1/job/{job_id}")
        return self._parse_task_response(data)

    async def _fetch_task(self, job_id: str) -> TaskResponse:
        """Fetch task (async)."""
        return await self.get(job_id)

    async def _sleep(self, duration: float) -> None:
        """Sleep (async)."""
        await asyncio.sleep(duration)

    async def wait_for_completion(
        self,
        job_id: str,
        *,
        timeout: float = 300.0,
        poll_interval: float = 3.0,
        on_progress: Optional[Callable[[TaskResponse], None]] = None,
    ) -> TaskResponse:
        """Wait for a task to complete (async).

        Args:
            job_id: The job ID to wait for
            timeout: Maximum time to wait in seconds (default: 300)
            poll_interval: Time between status checks in seconds (default: 3)
            on_progress: Optional callback called on each status check

        Returns:
            Completed task response

        Raises:
            TimeoutError: If task doesn't complete within timeout
            LegnextAPIError: If task fails
        """
        return await self._wait_for_completion_impl(job_id, timeout, poll_interval, on_progress)

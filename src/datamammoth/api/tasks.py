"""Tasks API — poll async tasks for long-running operations."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.common import Task


class TasksAPI:
    """Synchronous tasks API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_type: Optional[str] = None,
    ) -> List[Task]:
        """List tasks."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_type:
            params["filter[type]"] = filter_type
        data = self._client.get("/tasks", params=params)
        return [Task(**t) for t in data]

    def list_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all tasks."""
        return PageIterator(self._client, "/tasks", params=kwargs, model=Task)

    def get(self, task_id: str) -> Task:
        """Get a single task by ID."""
        return Task(**self._client.get(f"/tasks/{task_id}"))

    def wait(
        self,
        task_id: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Task:
        """Poll a task until it completes or times out.

        Args:
            task_id: The task ID to poll.
            poll_interval: Seconds between polls.
            timeout: Max seconds to wait.

        Returns:
            The completed Task.

        Raises:
            TimeoutError: If the task does not complete within the timeout.
        """
        import time

        start = time.monotonic()
        while True:
            task = self.get(task_id)
            if task.status in ("completed", "failed", "cancelled"):
                return task
            elapsed = time.monotonic() - start
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Task {task_id} did not complete within {timeout}s (status: {task.status})"
                )
            time.sleep(poll_interval)


class AsyncTasksAPI:
    """Asynchronous tasks API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_type: Optional[str] = None,
    ) -> List[Task]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_type:
            params["filter[type]"] = filter_type
        data = await self._client.get("/tasks", params=params)
        return [Task(**t) for t in data]

    def list_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/tasks", params=kwargs, model=Task)

    async def get(self, task_id: str) -> Task:
        return Task(**await self._client.get(f"/tasks/{task_id}"))

    async def wait(
        self,
        task_id: str,
        poll_interval: float = 2.0,
        timeout: float = 300.0,
    ) -> Task:
        """Poll a task until it completes or times out."""
        import asyncio
        import time

        start = time.monotonic()
        while True:
            task = await self.get(task_id)
            if task.status in ("completed", "failed", "cancelled"):
                return task
            elapsed = time.monotonic() - start
            if elapsed >= timeout:
                raise TimeoutError(
                    f"Task {task_id} did not complete within {timeout}s (status: {task.status})"
                )
            await asyncio.sleep(poll_interval)

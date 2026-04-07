"""Auto-pagination iterators for list endpoints."""

from typing import Any, Dict, Iterator, List, Optional, Type, TypeVar, AsyncIterator

T = TypeVar("T")


class PageIterator:
    """Synchronous iterator that auto-paginates through all pages.

    Usage::

        for server in dm.servers.list_all(filter_status="active"):
            print(server.hostname)
    """

    def __init__(
        self,
        client: Any,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ):
        self._client = client
        self._path = path
        self._params = dict(params or {})
        self._model = model
        self._page = 1
        self._has_next = True

    def __iter__(self) -> Iterator:
        self._page = 1
        self._has_next = True
        return self

    def __next__(self) -> Any:
        # We buffer items per page and yield one at a time
        if not hasattr(self, "_buffer") or not self._buffer:
            if not self._has_next:
                raise StopIteration
            self._fetch_page()
            if not self._buffer:
                raise StopIteration
        return self._buffer.pop(0)

    def _fetch_page(self) -> None:
        self._params["page"] = self._page
        resp = self._client.raw_get(self._path, params=self._params)
        items = resp.get("data", [])
        meta = resp.get("meta", {}).get("pagination", {})
        self._has_next = meta.get("has_next", False)
        self._page += 1

        if self._model and items:
            self._buffer: List[Any] = [self._model(**item) for item in items]
        else:
            self._buffer = list(items)

    def to_list(self) -> List[Any]:
        """Consume the entire iterator into a list."""
        return list(self)

    def first(self) -> Optional[Any]:
        """Return the first item or None."""
        for item in self:
            return item
        return None


class AsyncPageIterator:
    """Asynchronous iterator that auto-paginates through all pages.

    Usage::

        async for server in dm.servers.list_all(filter_status="active"):
            print(server.hostname)
    """

    def __init__(
        self,
        client: Any,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        model: Optional[Type[T]] = None,
    ):
        self._client = client
        self._path = path
        self._params = dict(params or {})
        self._model = model
        self._page = 1
        self._has_next = True
        self._buffer: List[Any] = []

    def __aiter__(self) -> "AsyncPageIterator":
        self._page = 1
        self._has_next = True
        self._buffer = []
        return self

    async def __anext__(self) -> Any:
        if not self._buffer:
            if not self._has_next:
                raise StopAsyncIteration
            await self._fetch_page()
            if not self._buffer:
                raise StopAsyncIteration
        return self._buffer.pop(0)

    async def _fetch_page(self) -> None:
        self._params["page"] = self._page
        resp = await self._client.raw_get(self._path, params=self._params)
        items = resp.get("data", [])
        meta = resp.get("meta", {}).get("pagination", {})
        self._has_next = meta.get("has_next", False)
        self._page += 1

        if self._model and items:
            self._buffer = [self._model(**item) for item in items]
        else:
            self._buffer = list(items)

    async def to_list(self) -> List[Any]:
        """Consume the entire iterator into a list."""
        result = []
        async for item in self:
            result.append(item)
        return result

    async def first(self) -> Optional[Any]:
        """Return the first item or None."""
        async for item in self:
            return item
        return None

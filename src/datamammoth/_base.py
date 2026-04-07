"""Base HTTP client with shared logic for sync and async clients."""

from typing import Any, Dict, Optional

import httpx

from datamammoth.exceptions import RateLimitError, map_error

_USER_AGENT = "datamammoth-python/0.1.0"


class _BaseClient:
    """Synchronous HTTP client wrapping httpx.Client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.datamammoth.com/api/v2",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": _USER_AGENT,
            },
            timeout=timeout,
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request."""
        resp = self.session.get(path, params=params)
        return self._handle(resp)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a POST request."""
        resp = self.session.post(path, json=json)
        return self._handle(resp)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a PATCH request."""
        resp = self.session.patch(path, json=json)
        return self._handle(resp)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a PUT request."""
        resp = self.session.put(path, json=json)
        return self._handle(resp)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a DELETE request."""
        resp = self.session.delete(path, params=params)
        return self._handle(resp)

    def _handle(self, resp: httpx.Response) -> Any:
        """Process an HTTP response, raising on errors."""
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            body = resp.json() if resp.content else {}
            raise map_error(429, body, retry_after=retry_seconds)

        if resp.status_code == 204:
            return None

        body = resp.json() if resp.content else {}

        if resp.status_code >= 400:
            raise map_error(resp.status_code, body)

        # V2 responses wrap data in {"data": ...}
        return body.get("data", body)

    def raw_get(self, path: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """GET that returns the full response body (including meta)."""
        resp = self.session.get(path, params=params)
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            body = resp.json() if resp.content else {}
            raise map_error(429, body, retry_after=retry_seconds)
        if resp.status_code >= 400:
            body = resp.json() if resp.content else {}
            raise map_error(resp.status_code, body)
        return resp.json()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

    def __enter__(self) -> "_BaseClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class _AsyncBaseClient:
    """Asynchronous HTTP client wrapping httpx.AsyncClient."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.datamammoth.com/api/v2",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": _USER_AGENT,
            },
            timeout=timeout,
        )

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a GET request."""
        resp = await self.session.get(path, params=params)
        return self._handle(resp)

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a POST request."""
        resp = await self.session.post(path, json=json)
        return self._handle(resp)

    async def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a PATCH request."""
        resp = await self.session.patch(path, json=json)
        return self._handle(resp)

    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        """Send a PUT request."""
        resp = await self.session.put(path, json=json)
        return self._handle(resp)

    async def delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Send a DELETE request."""
        resp = await self.session.delete(path, params=params)
        return self._handle(resp)

    def _handle(self, resp: httpx.Response) -> Any:
        """Process an HTTP response, raising on errors."""
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            body = resp.json() if resp.content else {}
            raise map_error(429, body, retry_after=retry_seconds)

        if resp.status_code == 204:
            return None

        body = resp.json() if resp.content else {}

        if resp.status_code >= 400:
            raise map_error(resp.status_code, body)

        return body.get("data", body)

    async def raw_get(self, path: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """GET that returns the full response body (including meta)."""
        resp = await self.session.get(path, params=params)
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            body = resp.json() if resp.content else {}
            raise map_error(429, body, retry_after=retry_seconds)
        if resp.status_code >= 400:
            body = resp.json() if resp.content else {}
            raise map_error(resp.status_code, body)
        return resp.json()

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self.session.aclose()

    async def __aenter__(self) -> "_AsyncBaseClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

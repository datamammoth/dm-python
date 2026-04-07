"""Asynchronous DataMammoth client — async/await version of the SDK."""

from typing import Any, Optional

from datamammoth._base import _AsyncBaseClient
from datamammoth.api.account import AsyncAccountAPI
from datamammoth.api.admin import AsyncAdminAPI
from datamammoth.api.affiliate import AsyncAffiliateAPI
from datamammoth.api.billing import AsyncBillingAPI
from datamammoth.api.products import AsyncProductsAPI
from datamammoth.api.servers import AsyncServersAPI
from datamammoth.api.support import AsyncSupportAPI
from datamammoth.api.tasks import AsyncTasksAPI
from datamammoth.api.webhooks import AsyncWebhooksAPI
from datamammoth.api.zones import AsyncZonesAPI


class AsyncDataMammoth:
    """Asynchronous client for the DataMammoth API v2.

    Usage::

        import asyncio
        from datamammoth import AsyncDataMammoth

        async def main():
            async with AsyncDataMammoth(api_key="dm_your_key_here") as dm:
                servers = await dm.servers.list(filter_status="active")
                for server in servers:
                    print(f"{server.hostname} -- {server.ip_address}")

        asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.datamammoth.com/api/v2",
        timeout: int = 30,
    ):
        """Initialize the async DataMammoth client.

        Args:
            api_key: Your DataMammoth API key (starts with ``dm_``).
            base_url: Base URL for the API. Override for self-hosted or staging.
            timeout: Request timeout in seconds (default 30).
        """
        self._client = _AsyncBaseClient(api_key=api_key, base_url=base_url, timeout=timeout)

        # Attach API resource namespaces
        self.servers = AsyncServersAPI(self._client)
        self.products = AsyncProductsAPI(self._client)
        self.billing = AsyncBillingAPI(self._client)
        self.support = AsyncSupportAPI(self._client)
        self.account = AsyncAccountAPI(self._client)
        self.admin = AsyncAdminAPI(self._client)
        self.affiliate = AsyncAffiliateAPI(self._client)
        self.webhooks = AsyncWebhooksAPI(self._client)
        self.tasks = AsyncTasksAPI(self._client)
        self.zones = AsyncZonesAPI(self._client)

    async def health(self) -> dict:
        """Check API health status."""
        return await self._client.get("/health")

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._client.close()

    async def __aenter__(self) -> "AsyncDataMammoth":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"<AsyncDataMammoth base_url={self._client.base_url!r}>"

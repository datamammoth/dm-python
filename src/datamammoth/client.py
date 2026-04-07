"""Synchronous DataMammoth client — the main entry point for the SDK."""

from typing import Any, Optional

from datamammoth._base import _BaseClient
from datamammoth.api.account import AccountAPI
from datamammoth.api.admin import AdminAPI
from datamammoth.api.affiliate import AffiliateAPI
from datamammoth.api.billing import BillingAPI
from datamammoth.api.products import ProductsAPI
from datamammoth.api.servers import ServersAPI
from datamammoth.api.support import SupportAPI
from datamammoth.api.tasks import TasksAPI
from datamammoth.api.webhooks import WebhooksAPI
from datamammoth.api.zones import ZonesAPI


class DataMammoth:
    """Synchronous client for the DataMammoth API v2.

    Usage::

        from datamammoth import DataMammoth

        dm = DataMammoth(api_key="dm_your_key_here")
        servers = dm.servers.list(filter_status="active")
        for server in servers:
            print(f"{server.hostname} -- {server.ip_address}")

    Or as a context manager::

        with DataMammoth(api_key="dm_key") as dm:
            profile = dm.account.me()
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.datamammoth.com/api/v2",
        timeout: int = 30,
    ):
        """Initialize the DataMammoth client.

        Args:
            api_key: Your DataMammoth API key (starts with ``dm_``).
            base_url: Base URL for the API. Override for self-hosted or staging.
            timeout: Request timeout in seconds (default 30).
        """
        self._client = _BaseClient(api_key=api_key, base_url=base_url, timeout=timeout)

        # Attach API resource namespaces
        self.servers = ServersAPI(self._client)
        self.products = ProductsAPI(self._client)
        self.billing = BillingAPI(self._client)
        self.support = SupportAPI(self._client)
        self.account = AccountAPI(self._client)
        self.admin = AdminAPI(self._client)
        self.affiliate = AffiliateAPI(self._client)
        self.webhooks = WebhooksAPI(self._client)
        self.tasks = TasksAPI(self._client)
        self.zones = ZonesAPI(self._client)

    def health(self) -> dict:
        """Check API health status."""
        return self._client.get("/health")

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> "DataMammoth":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"<DataMammoth base_url={self._client.base_url!r}>"

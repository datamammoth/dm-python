"""Webhooks API — register endpoints, view deliveries, test."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.webhook import EventType, Webhook, WebhookDelivery


class WebhooksAPI:
    """Synchronous webhooks API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Webhooks CRUD ────────────────────────────────────────────────

    def list(
        self,
        page: int = 1,
        per_page: int = 20,
    ) -> List[Webhook]:
        """List registered webhooks."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = self._client.get("/webhooks", params=params)
        return [Webhook(**w) for w in data]

    def get(self, webhook_id: str) -> Webhook:
        """Get a single webhook."""
        return Webhook(**self._client.get(f"/webhooks/{webhook_id}"))

    def create(
        self,
        url: str,
        events: List[str],
        description: Optional[str] = None,
        secret: Optional[str] = None,
        is_active: bool = True,
    ) -> Webhook:
        """Register a new webhook endpoint."""
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
            "is_active": is_active,
        }
        if description:
            body["description"] = description
        if secret:
            body["secret"] = secret
        return Webhook(**self._client.post("/webhooks", json=body))

    def update(self, webhook_id: str, **fields: Any) -> Webhook:
        """Update a webhook."""
        return Webhook(**self._client.patch(f"/webhooks/{webhook_id}", json=fields))

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook."""
        self._client.delete(f"/webhooks/{webhook_id}")

    # ── Deliveries ───────────────────────────────────────────────────

    def deliveries(
        self,
        webhook_id: str,
        page: int = 1,
        per_page: int = 20,
    ) -> List[WebhookDelivery]:
        """List delivery attempts for a webhook."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = self._client.get(f"/webhooks/{webhook_id}/deliveries", params=params)
        return [WebhookDelivery(**d) for d in data]

    # ── Test ─────────────────────────────────────────────────────────

    def test(self, webhook_id: str) -> WebhookDelivery:
        """Send a test payload to a webhook endpoint."""
        return WebhookDelivery(
            **self._client.post(f"/webhooks/{webhook_id}/test")
        )

    # ── Event Types ──────────────────────────────────────────────────

    def event_types(self) -> List[EventType]:
        """List all available webhook event types."""
        data = self._client.get("/webhooks/events")
        return [EventType(**e) for e in data]


class AsyncWebhooksAPI:
    """Asynchronous webhooks API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def list(self, page: int = 1, per_page: int = 20) -> List[Webhook]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = await self._client.get("/webhooks", params=params)
        return [Webhook(**w) for w in data]

    async def get(self, webhook_id: str) -> Webhook:
        return Webhook(**await self._client.get(f"/webhooks/{webhook_id}"))

    async def create(
        self,
        url: str,
        events: List[str],
        description: Optional[str] = None,
        secret: Optional[str] = None,
        is_active: bool = True,
    ) -> Webhook:
        body: Dict[str, Any] = {
            "url": url,
            "events": events,
            "is_active": is_active,
        }
        if description:
            body["description"] = description
        if secret:
            body["secret"] = secret
        return Webhook(**await self._client.post("/webhooks", json=body))

    async def update(self, webhook_id: str, **fields: Any) -> Webhook:
        return Webhook(**await self._client.patch(f"/webhooks/{webhook_id}", json=fields))

    async def delete(self, webhook_id: str) -> None:
        await self._client.delete(f"/webhooks/{webhook_id}")

    async def deliveries(
        self, webhook_id: str, page: int = 1, per_page: int = 20
    ) -> List[WebhookDelivery]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        data = await self._client.get(f"/webhooks/{webhook_id}/deliveries", params=params)
        return [WebhookDelivery(**d) for d in data]

    async def test(self, webhook_id: str) -> WebhookDelivery:
        return WebhookDelivery(**await self._client.post(f"/webhooks/{webhook_id}/test"))

    async def event_types(self) -> List[EventType]:
        data = await self._client.get("/webhooks/events")
        return [EventType(**e) for e in data]

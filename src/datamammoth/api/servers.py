"""Servers API — provision, manage, and monitor servers."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.common import Task
from datamammoth.models.server import (
    ConsoleSession,
    FirewallRule,
    Metric,
    Server,
    ServerEvent,
    Snapshot,
)


class ServersAPI:
    """Synchronous servers API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── List / Get ───────────────────────────────────────────────────

    def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_region: Optional[str] = None,
    ) -> List[Server]:
        """List servers with pagination, sorting, and filtering."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_region:
            params["filter[region]"] = filter_region
        data = self._client.get("/servers", params=params)
        return [Server(**s) for s in data]

    def list_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all servers."""
        return PageIterator(self._client, "/servers", params=kwargs, model=Server)

    def get(self, server_id: str) -> Server:
        """Get a single server by ID."""
        return Server(**self._client.get(f"/servers/{server_id}"))

    # ── Create / Delete ──────────────────────────────────────────────

    def create(
        self,
        product_id: str,
        image_id: str,
        hostname: Optional[str] = None,
        region: Optional[str] = None,
        label: Optional[str] = None,
        ssh_key_ids: Optional[List[str]] = None,
        addons: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """Create (provision) a new server. Returns an async Task."""
        body: Dict[str, Any] = {"product_id": product_id, "image_id": image_id}
        if hostname:
            body["hostname"] = hostname
        if region:
            body["region"] = region
        if label:
            body["label"] = label
        if ssh_key_ids:
            body["ssh_key_ids"] = ssh_key_ids
        if addons:
            body["addons"] = addons
        if options:
            body["options"] = options
        return Task(**self._client.post("/servers", json=body))

    def delete(self, server_id: str) -> Task:
        """Delete (destroy) a server. Returns an async Task."""
        return Task(**self._client.delete(f"/servers/{server_id}"))

    # ── Power actions ────────────────────────────────────────────────

    def power_on(self, server_id: str) -> Task:
        """Power on a server."""
        return Task(**self._client.post(f"/servers/{server_id}/actions/power-on"))

    def power_off(self, server_id: str) -> Task:
        """Power off a server (hard)."""
        return Task(**self._client.post(f"/servers/{server_id}/actions/power-off"))

    def reboot(self, server_id: str) -> Task:
        """Reboot a server (hard)."""
        return Task(**self._client.post(f"/servers/{server_id}/actions/reboot"))

    def shutdown(self, server_id: str) -> Task:
        """Gracefully shut down a server."""
        return Task(**self._client.post(f"/servers/{server_id}/actions/shutdown"))

    def rebuild(self, server_id: str, image_id: str) -> Task:
        """Rebuild a server with a new OS image."""
        return Task(
            **self._client.post(
                f"/servers/{server_id}/actions/rebuild",
                json={"image_id": image_id},
            )
        )

    def rescue(self, server_id: str, root_password: Optional[str] = None) -> Task:
        """Boot a server into rescue mode."""
        body: Dict[str, Any] = {}
        if root_password:
            body["root_password"] = root_password
        return Task(
            **self._client.post(f"/servers/{server_id}/actions/rescue", json=body)
        )

    def reinstall(self, server_id: str, image_id: str) -> Task:
        """Reinstall a server with a new OS image."""
        return Task(
            **self._client.post(
                f"/servers/{server_id}/actions/reinstall",
                json={"image_id": image_id},
            )
        )

    # ── Snapshots ────────────────────────────────────────────────────

    def snapshots(self, server_id: str) -> List[Snapshot]:
        """List snapshots for a server."""
        data = self._client.get(f"/servers/{server_id}/snapshots")
        return [Snapshot(**s) for s in data]

    def create_snapshot(self, server_id: str, name: str) -> Snapshot:
        """Create a snapshot of a server."""
        return Snapshot(
            **self._client.post(
                f"/servers/{server_id}/snapshots", json={"name": name}
            )
        )

    def delete_snapshot(self, server_id: str, snapshot_id: str) -> None:
        """Delete a snapshot."""
        self._client.delete(f"/servers/{server_id}/snapshots/{snapshot_id}")

    def restore_snapshot(self, server_id: str, snapshot_id: str) -> Task:
        """Restore a server from a snapshot."""
        return Task(
            **self._client.post(
                f"/servers/{server_id}/snapshots/{snapshot_id}",
                json={"action": "restore"},
            )
        )

    # ── Metrics / Events / Console ───────────────────────────────────

    def metrics(
        self, server_id: str, period: str = "24h"
    ) -> List[Metric]:
        """Get server resource metrics."""
        data = self._client.get(
            f"/servers/{server_id}/metrics", params={"period": period}
        )
        return [Metric(**m) for m in data]

    def events(self, server_id: str) -> List[ServerEvent]:
        """List server events / activity log."""
        data = self._client.get(f"/servers/{server_id}/events")
        return [ServerEvent(**e) for e in data]

    def console(self, server_id: str) -> ConsoleSession:
        """Get a VNC/noVNC console session URL."""
        return ConsoleSession(**self._client.get(f"/servers/{server_id}/console"))

    # ── Firewall ─────────────────────────────────────────────────────

    def firewall(self, server_id: str) -> List[FirewallRule]:
        """Get the current firewall rules."""
        data = self._client.get(f"/servers/{server_id}/firewall")
        return [FirewallRule(**r) for r in data]

    def update_firewall(
        self, server_id: str, rules: List[Dict[str, Any]]
    ) -> List[FirewallRule]:
        """Replace all firewall rules."""
        data = self._client.put(
            f"/servers/{server_id}/firewall", json={"rules": rules}
        )
        return [FirewallRule(**r) for r in data]


class AsyncServersAPI:
    """Asynchronous servers API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_region: Optional[str] = None,
    ) -> List[Server]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_region:
            params["filter[region]"] = filter_region
        data = await self._client.get("/servers", params=params)
        return [Server(**s) for s in data]

    def list_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/servers", params=kwargs, model=Server)

    async def get(self, server_id: str) -> Server:
        return Server(**await self._client.get(f"/servers/{server_id}"))

    async def create(
        self,
        product_id: str,
        image_id: str,
        hostname: Optional[str] = None,
        region: Optional[str] = None,
        label: Optional[str] = None,
        ssh_key_ids: Optional[List[str]] = None,
        addons: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> Task:
        body: Dict[str, Any] = {"product_id": product_id, "image_id": image_id}
        if hostname:
            body["hostname"] = hostname
        if region:
            body["region"] = region
        if label:
            body["label"] = label
        if ssh_key_ids:
            body["ssh_key_ids"] = ssh_key_ids
        if addons:
            body["addons"] = addons
        if options:
            body["options"] = options
        return Task(**await self._client.post("/servers", json=body))

    async def delete(self, server_id: str) -> Task:
        return Task(**await self._client.delete(f"/servers/{server_id}"))

    async def power_on(self, server_id: str) -> Task:
        return Task(**await self._client.post(f"/servers/{server_id}/actions/power-on"))

    async def power_off(self, server_id: str) -> Task:
        return Task(**await self._client.post(f"/servers/{server_id}/actions/power-off"))

    async def reboot(self, server_id: str) -> Task:
        return Task(**await self._client.post(f"/servers/{server_id}/actions/reboot"))

    async def shutdown(self, server_id: str) -> Task:
        return Task(**await self._client.post(f"/servers/{server_id}/actions/shutdown"))

    async def rebuild(self, server_id: str, image_id: str) -> Task:
        return Task(
            **await self._client.post(
                f"/servers/{server_id}/actions/rebuild", json={"image_id": image_id}
            )
        )

    async def rescue(self, server_id: str, root_password: Optional[str] = None) -> Task:
        body: Dict[str, Any] = {}
        if root_password:
            body["root_password"] = root_password
        return Task(
            **await self._client.post(f"/servers/{server_id}/actions/rescue", json=body)
        )

    async def reinstall(self, server_id: str, image_id: str) -> Task:
        return Task(
            **await self._client.post(
                f"/servers/{server_id}/actions/reinstall", json={"image_id": image_id}
            )
        )

    async def snapshots(self, server_id: str) -> List[Snapshot]:
        data = await self._client.get(f"/servers/{server_id}/snapshots")
        return [Snapshot(**s) for s in data]

    async def create_snapshot(self, server_id: str, name: str) -> Snapshot:
        return Snapshot(
            **await self._client.post(
                f"/servers/{server_id}/snapshots", json={"name": name}
            )
        )

    async def delete_snapshot(self, server_id: str, snapshot_id: str) -> None:
        await self._client.delete(f"/servers/{server_id}/snapshots/{snapshot_id}")

    async def restore_snapshot(self, server_id: str, snapshot_id: str) -> Task:
        return Task(
            **await self._client.post(
                f"/servers/{server_id}/snapshots/{snapshot_id}",
                json={"action": "restore"},
            )
        )

    async def metrics(self, server_id: str, period: str = "24h") -> List[Metric]:
        data = await self._client.get(
            f"/servers/{server_id}/metrics", params={"period": period}
        )
        return [Metric(**m) for m in data]

    async def events(self, server_id: str) -> List[ServerEvent]:
        data = await self._client.get(f"/servers/{server_id}/events")
        return [ServerEvent(**e) for e in data]

    async def console(self, server_id: str) -> ConsoleSession:
        return ConsoleSession(**await self._client.get(f"/servers/{server_id}/console"))

    async def firewall(self, server_id: str) -> List[FirewallRule]:
        data = await self._client.get(f"/servers/{server_id}/firewall")
        return [FirewallRule(**r) for r in data]

    async def update_firewall(
        self, server_id: str, rules: List[Dict[str, Any]]
    ) -> List[FirewallRule]:
        data = await self._client.put(
            f"/servers/{server_id}/firewall", json={"rules": rules}
        )
        return [FirewallRule(**r) for r in data]

"""Admin API — users, roles, tenants, leads, audit log, dashboard stats."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.admin import (
    AdminUser,
    AuditLogEntry,
    DashboardStats,
    Lead,
    Role,
    Tenant,
)
from datamammoth.models.billing import Invoice
from datamammoth.models.server import Server
from datamammoth.models.support import Ticket


class AdminAPI:
    """Synchronous admin API (requires admin role)."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Users ────────────────────────────────────────────────────────

    def users(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_role: Optional[str] = None,
    ) -> List[AdminUser]:
        """List all users."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_role:
            params["filter[role]"] = filter_role
        data = self._client.get("/admin/users", params=params)
        return [AdminUser(**u) for u in data]

    def users_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all users."""
        return PageIterator(self._client, "/admin/users", params=kwargs, model=AdminUser)

    def get_user(self, user_id: str) -> AdminUser:
        """Get a single user."""
        return AdminUser(**self._client.get(f"/admin/users/{user_id}"))

    def update_user(self, user_id: str, **fields: Any) -> AdminUser:
        """Update a user's fields (status, role, etc.)."""
        return AdminUser(**self._client.patch(f"/admin/users/{user_id}", json=fields))

    def masquerade(self, user_id: str) -> dict:
        """Masquerade as a user (admin impersonation)."""
        return self._client.post(f"/admin/masquerade/{user_id}")

    # ── Roles ────────────────────────────────────────────────────────

    def roles(self) -> List[Role]:
        """List all roles."""
        data = self._client.get("/admin/roles")
        return [Role(**r) for r in data]

    def get_role(self, role_id: str) -> Role:
        """Get a single role."""
        return Role(**self._client.get(f"/admin/roles/{role_id}"))

    def create_role(
        self,
        name: str,
        permissions: List[str],
        description: Optional[str] = None,
    ) -> Role:
        """Create a new role."""
        body: Dict[str, Any] = {"name": name, "permissions": permissions}
        if description:
            body["description"] = description
        return Role(**self._client.post("/admin/roles", json=body))

    def update_role(self, role_id: str, **fields: Any) -> Role:
        """Update a role."""
        return Role(**self._client.patch(f"/admin/roles/{role_id}", json=fields))

    def delete_role(self, role_id: str) -> None:
        """Delete a role."""
        self._client.delete(f"/admin/roles/{role_id}")

    # ── Tenants ──────────────────────────────────────────────────────

    def tenants(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
    ) -> List[Tenant]:
        """List all tenants."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        data = self._client.get("/admin/tenants", params=params)
        return [Tenant(**t) for t in data]

    def get_tenant(self, tenant_id: str) -> Tenant:
        """Get a single tenant."""
        return Tenant(**self._client.get(f"/admin/tenants/{tenant_id}"))

    def update_tenant(self, tenant_id: str, **fields: Any) -> Tenant:
        """Update a tenant."""
        return Tenant(**self._client.patch(f"/admin/tenants/{tenant_id}", json=fields))

    # ── Admin Invoices ───────────────────────────────────────────────

    def invoices(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> List[Invoice]:
        """List all invoices (admin view)."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_user:
            params["filter[user]"] = filter_user
        data = self._client.get("/admin/invoices", params=params)
        return [Invoice(**i) for i in data]

    # ── Admin Servers ────────────────────────────────────────────────

    def servers(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> List[Server]:
        """List all servers (admin view)."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_user:
            params["filter[user]"] = filter_user
        data = self._client.get("/admin/servers", params=params)
        return [Server(**s) for s in data]

    # ── Admin Tickets ────────────────────────────────────────────────

    def tickets(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_department: Optional[str] = None,
        filter_assigned: Optional[str] = None,
    ) -> List[Ticket]:
        """List all tickets (admin view)."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_department:
            params["filter[department]"] = filter_department
        if filter_assigned:
            params["filter[assigned]"] = filter_assigned
        data = self._client.get("/admin/tickets", params=params)
        return [Ticket(**t) for t in data]

    def get_ticket(self, ticket_id: str) -> Ticket:
        """Get a single ticket (admin view)."""
        return Ticket(**self._client.get(f"/admin/tickets/{ticket_id}"))

    def update_ticket(self, ticket_id: str, **fields: Any) -> Ticket:
        """Update a ticket (assign, change status/priority, etc.)."""
        return Ticket(**self._client.patch(f"/admin/tickets/{ticket_id}", json=fields))

    # ── Leads ────────────────────────────────────────────────────────

    def leads(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_score: Optional[str] = None,
        filter_status: Optional[str] = None,
    ) -> List[Lead]:
        """List marketing leads."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_score:
            params["filter[score]"] = filter_score
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/admin/leads", params=params)
        return [Lead(**l) for l in data]

    # ── Audit Log ────────────────────────────────────────────────────

    def audit_log(
        self,
        page: int = 1,
        per_page: int = 50,
        sort: str = "-created_at",
        filter_action: Optional[str] = None,
        filter_actor: Optional[str] = None,
    ) -> List[AuditLogEntry]:
        """List admin audit log entries."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_action:
            params["filter[action]"] = filter_action
        if filter_actor:
            params["filter[actor]"] = filter_actor
        data = self._client.get("/admin/audit-log", params=params)
        return [AuditLogEntry(**e) for e in data]

    # ── Dashboard ────────────────────────────────────────────────────

    def dashboard_stats(self) -> DashboardStats:
        """Get admin dashboard summary statistics."""
        return DashboardStats(**self._client.get("/admin/dashboard/stats"))

    # ── V1 Usage (migration) ─────────────────────────────────────────

    def v1_usage(self) -> dict:
        """Get API v1 usage statistics (for migration tracking)."""
        return self._client.get("/admin/v1-usage")


class AsyncAdminAPI:
    """Asynchronous admin API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def users(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_role: Optional[str] = None,
    ) -> List[AdminUser]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_role:
            params["filter[role]"] = filter_role
        data = await self._client.get("/admin/users", params=params)
        return [AdminUser(**u) for u in data]

    def users_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/admin/users", params=kwargs, model=AdminUser)

    async def get_user(self, user_id: str) -> AdminUser:
        return AdminUser(**await self._client.get(f"/admin/users/{user_id}"))

    async def update_user(self, user_id: str, **fields: Any) -> AdminUser:
        return AdminUser(**await self._client.patch(f"/admin/users/{user_id}", json=fields))

    async def masquerade(self, user_id: str) -> dict:
        return await self._client.post(f"/admin/masquerade/{user_id}")

    async def roles(self) -> List[Role]:
        data = await self._client.get("/admin/roles")
        return [Role(**r) for r in data]

    async def get_role(self, role_id: str) -> Role:
        return Role(**await self._client.get(f"/admin/roles/{role_id}"))

    async def create_role(
        self, name: str, permissions: List[str], description: Optional[str] = None
    ) -> Role:
        body: Dict[str, Any] = {"name": name, "permissions": permissions}
        if description:
            body["description"] = description
        return Role(**await self._client.post("/admin/roles", json=body))

    async def update_role(self, role_id: str, **fields: Any) -> Role:
        return Role(**await self._client.patch(f"/admin/roles/{role_id}", json=fields))

    async def delete_role(self, role_id: str) -> None:
        await self._client.delete(f"/admin/roles/{role_id}")

    async def tenants(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> List[Tenant]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        data = await self._client.get("/admin/tenants", params=params)
        return [Tenant(**t) for t in data]

    async def get_tenant(self, tenant_id: str) -> Tenant:
        return Tenant(**await self._client.get(f"/admin/tenants/{tenant_id}"))

    async def update_tenant(self, tenant_id: str, **fields: Any) -> Tenant:
        return Tenant(**await self._client.patch(f"/admin/tenants/{tenant_id}", json=fields))

    async def invoices(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> List[Invoice]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_user:
            params["filter[user]"] = filter_user
        data = await self._client.get("/admin/invoices", params=params)
        return [Invoice(**i) for i in data]

    async def servers(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_status: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> List[Server]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_user:
            params["filter[user]"] = filter_user
        data = await self._client.get("/admin/servers", params=params)
        return [Server(**s) for s in data]

    async def tickets(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_department: Optional[str] = None,
        filter_assigned: Optional[str] = None,
    ) -> List[Ticket]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_department:
            params["filter[department]"] = filter_department
        if filter_assigned:
            params["filter[assigned]"] = filter_assigned
        data = await self._client.get("/admin/tickets", params=params)
        return [Ticket(**t) for t in data]

    async def get_ticket(self, ticket_id: str) -> Ticket:
        return Ticket(**await self._client.get(f"/admin/tickets/{ticket_id}"))

    async def update_ticket(self, ticket_id: str, **fields: Any) -> Ticket:
        return Ticket(**await self._client.patch(f"/admin/tickets/{ticket_id}", json=fields))

    async def leads(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        search: Optional[str] = None,
        filter_score: Optional[str] = None,
        filter_status: Optional[str] = None,
    ) -> List[Lead]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_score:
            params["filter[score]"] = filter_score
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/admin/leads", params=params)
        return [Lead(**l) for l in data]

    async def audit_log(
        self,
        page: int = 1,
        per_page: int = 50,
        sort: str = "-created_at",
        filter_action: Optional[str] = None,
        filter_actor: Optional[str] = None,
    ) -> List[AuditLogEntry]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_action:
            params["filter[action]"] = filter_action
        if filter_actor:
            params["filter[actor]"] = filter_actor
        data = await self._client.get("/admin/audit-log", params=params)
        return [AuditLogEntry(**e) for e in data]

    async def dashboard_stats(self) -> DashboardStats:
        return DashboardStats(**await self._client.get("/admin/dashboard/stats"))

    async def v1_usage(self) -> dict:
        return await self._client.get("/admin/v1-usage")

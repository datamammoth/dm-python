"""Support API — tickets, replies, departments, knowledge base."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.support import (
    Department,
    KBArticle,
    Ticket,
    TicketFeedback,
    TicketReply,
)


class SupportAPI:
    """Synchronous support API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Tickets ──────────────────────────────────────────────────────

    def tickets(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_department: Optional[str] = None,
        filter_priority: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Ticket]:
        """List support tickets."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_department:
            params["filter[department]"] = filter_department
        if filter_priority:
            params["filter[priority]"] = filter_priority
        if search:
            params["search"] = search
        data = self._client.get("/tickets", params=params)
        return [Ticket(**t) for t in data]

    def tickets_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all tickets."""
        return PageIterator(self._client, "/tickets", params=kwargs, model=Ticket)

    def get_ticket(self, ticket_id: str) -> Ticket:
        """Get a single ticket with replies."""
        return Ticket(**self._client.get(f"/tickets/{ticket_id}"))

    def create_ticket(
        self,
        subject: str,
        body: str,
        department_id: Optional[str] = None,
        priority: str = "medium",
        server_id: Optional[str] = None,
    ) -> Ticket:
        """Create a new support ticket."""
        payload: Dict[str, Any] = {
            "subject": subject,
            "body": body,
            "priority": priority,
        }
        if department_id:
            payload["department_id"] = department_id
        if server_id:
            payload["server_id"] = server_id
        return Ticket(**self._client.post("/tickets", json=payload))

    def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Ticket:
        """Update ticket status or priority."""
        body: Dict[str, Any] = {}
        if status:
            body["status"] = status
        if priority:
            body["priority"] = priority
        return Ticket(**self._client.patch(f"/tickets/{ticket_id}", json=body))

    def close_ticket(self, ticket_id: str) -> Ticket:
        """Close a ticket."""
        return self.update_ticket(ticket_id, status="closed")

    # ── Replies ──────────────────────────────────────────────────────

    def replies(self, ticket_id: str) -> List[TicketReply]:
        """List replies on a ticket."""
        data = self._client.get(f"/tickets/{ticket_id}/replies")
        return [TicketReply(**r) for r in data]

    def create_reply(self, ticket_id: str, body: str) -> TicketReply:
        """Add a reply to a ticket."""
        return TicketReply(
            **self._client.post(f"/tickets/{ticket_id}/replies", json={"body": body})
        )

    # ── Feedback ─────────────────────────────────────────────────────

    def submit_feedback(
        self, ticket_id: str, rating: int, comment: Optional[str] = None
    ) -> TicketFeedback:
        """Submit feedback on a closed ticket."""
        payload: Dict[str, Any] = {"rating": rating}
        if comment:
            payload["comment"] = comment
        return TicketFeedback(
            **self._client.post(f"/tickets/{ticket_id}/feedback", json=payload)
        )

    # ── Departments ──────────────────────────────────────────────────

    def departments(self) -> List[Department]:
        """List available departments."""
        data = self._client.get("/tickets/departments")
        return [Department(**d) for d in data]

    # ── Knowledge Base ───────────────────────────────────────────────

    def kb_articles(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
        filter_category: Optional[str] = None,
    ) -> List[KBArticle]:
        """List knowledge base articles."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        if filter_category:
            params["filter[category]"] = filter_category
        data = self._client.get("/kb/articles", params=params)
        return [KBArticle(**a) for a in data]

    def get_kb_article(self, slug: str) -> KBArticle:
        """Get a knowledge base article by slug."""
        return KBArticle(**self._client.get(f"/kb/articles/{slug}"))


class AsyncSupportAPI:
    """Asynchronous support API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def tickets(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
        filter_department: Optional[str] = None,
        filter_priority: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Ticket]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        if filter_department:
            params["filter[department]"] = filter_department
        if filter_priority:
            params["filter[priority]"] = filter_priority
        if search:
            params["search"] = search
        data = await self._client.get("/tickets", params=params)
        return [Ticket(**t) for t in data]

    def tickets_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/tickets", params=kwargs, model=Ticket)

    async def get_ticket(self, ticket_id: str) -> Ticket:
        return Ticket(**await self._client.get(f"/tickets/{ticket_id}"))

    async def create_ticket(
        self,
        subject: str,
        body: str,
        department_id: Optional[str] = None,
        priority: str = "medium",
        server_id: Optional[str] = None,
    ) -> Ticket:
        payload: Dict[str, Any] = {
            "subject": subject,
            "body": body,
            "priority": priority,
        }
        if department_id:
            payload["department_id"] = department_id
        if server_id:
            payload["server_id"] = server_id
        return Ticket(**await self._client.post("/tickets", json=payload))

    async def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Ticket:
        body: Dict[str, Any] = {}
        if status:
            body["status"] = status
        if priority:
            body["priority"] = priority
        return Ticket(**await self._client.patch(f"/tickets/{ticket_id}", json=body))

    async def close_ticket(self, ticket_id: str) -> Ticket:
        return await self.update_ticket(ticket_id, status="closed")

    async def replies(self, ticket_id: str) -> List[TicketReply]:
        data = await self._client.get(f"/tickets/{ticket_id}/replies")
        return [TicketReply(**r) for r in data]

    async def create_reply(self, ticket_id: str, body: str) -> TicketReply:
        return TicketReply(
            **await self._client.post(f"/tickets/{ticket_id}/replies", json={"body": body})
        )

    async def submit_feedback(
        self, ticket_id: str, rating: int, comment: Optional[str] = None
    ) -> TicketFeedback:
        payload: Dict[str, Any] = {"rating": rating}
        if comment:
            payload["comment"] = comment
        return TicketFeedback(
            **await self._client.post(f"/tickets/{ticket_id}/feedback", json=payload)
        )

    async def departments(self) -> List[Department]:
        data = await self._client.get("/tickets/departments")
        return [Department(**d) for d in data]

    async def kb_articles(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
        filter_category: Optional[str] = None,
    ) -> List[KBArticle]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        if filter_category:
            params["filter[category]"] = filter_category
        data = await self._client.get("/kb/articles", params=params)
        return [KBArticle(**a) for a in data]

    async def get_kb_article(self, slug: str) -> KBArticle:
        return KBArticle(**await self._client.get(f"/kb/articles/{slug}"))

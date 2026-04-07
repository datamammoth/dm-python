"""Support ticket and knowledge base models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TicketReply:
    """A reply on a support ticket."""

    id: str = ""
    ticket_id: Optional[str] = None
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    author_role: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[str] = None


@dataclass
class Ticket:
    """A support ticket."""

    id: str = ""
    subject: Optional[str] = None
    status: str = "open"
    priority: str = "medium"
    department_id: Optional[str] = None
    department_name: Optional[str] = None
    server_id: Optional[str] = None
    body: Optional[str] = None
    replies: Optional[List[TicketReply]] = None
    last_reply_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self) -> None:
        if self.replies and isinstance(self.replies, list):
            self.replies = [
                TicketReply(**r) if isinstance(r, dict) else r for r in self.replies
            ]


@dataclass
class Department:
    """A support department."""

    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


@dataclass
class KBArticle:
    """A knowledge base article."""

    id: str = ""
    slug: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    views: int = 0
    helpful_count: int = 0
    published: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class TicketFeedback:
    """Feedback on a support ticket resolution."""

    ticket_id: Optional[str] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    created_at: Optional[str] = None

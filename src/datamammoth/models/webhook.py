"""Webhook models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Webhook:
    """A registered webhook endpoint."""

    id: str = ""
    url: Optional[str] = None
    events: Optional[List[str]] = None
    secret: Optional[str] = None
    is_active: bool = True
    description: Optional[str] = None
    failure_count: int = 0
    last_triggered_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class WebhookDelivery:
    """A single webhook delivery attempt."""

    id: str = ""
    webhook_id: Optional[str] = None
    event: Optional[str] = None
    request_url: Optional[str] = None
    request_headers: Optional[Dict[str, str]] = None
    request_body: Optional[Dict[str, Any]] = None
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    response_time_ms: Optional[int] = None
    success: bool = False
    created_at: Optional[str] = None


@dataclass
class EventType:
    """An available webhook event type."""

    name: str = ""
    description: Optional[str] = None
    category: Optional[str] = None
    example_payload: Optional[Dict[str, Any]] = None

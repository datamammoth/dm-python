"""Admin-only models (users, roles, tenants, leads, audit log)."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AdminUser:
    """A user as seen from the admin panel."""

    id: str = ""
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    status: str = "active"
    server_count: int = 0
    balance: Optional[float] = None
    last_login_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Role:
    """An admin role with permissions."""

    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    user_count: int = 0
    is_system: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Tenant:
    """A white-label tenant site."""

    id: str = ""
    name: Optional[str] = None
    domain: Optional[str] = None
    slug: Optional[str] = None
    status: str = "active"
    owner_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    branding: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Lead:
    """A marketing lead."""

    id: str = ""
    email: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    score: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class AuditLogEntry:
    """An entry in the admin audit log."""

    id: str = ""
    actor_id: Optional[str] = None
    actor_email: Optional[str] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class DashboardStats:
    """Admin dashboard summary statistics."""

    total_users: int = 0
    active_servers: int = 0
    total_revenue: Optional[float] = None
    mrr: Optional[float] = None
    open_tickets: int = 0
    pending_orders: int = 0
    new_signups_today: int = 0
    server_uptime_percent: Optional[float] = None
    revenue_trend: Optional[List[Dict[str, Any]]] = None

"""User account models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class UserProfile:
    """The authenticated user's profile."""

    id: str = ""
    email: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    two_factor_enabled: bool = False
    email_verified: bool = False
    avatar_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ApiKey:
    """An API key for programmatic access."""

    id: str = ""
    name: Optional[str] = None
    key_prefix: Optional[str] = None
    scopes: Optional[List[str]] = None
    last_used_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Session:
    """An active login session."""

    id: str = ""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    is_current: bool = False
    last_active_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Notification:
    """A user notification."""

    id: str = ""
    type: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    read: bool = False
    action_url: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Activity:
    """An activity log entry."""

    id: str = ""
    type: Optional[str] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


@dataclass
class TwoFactorStatus:
    """Two-factor authentication status and setup info."""

    enabled: bool = False
    method: Optional[str] = None
    provisioning_uri: Optional[str] = None
    backup_codes: Optional[List[str]] = None

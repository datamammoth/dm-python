"""Common response models shared across the API."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Pagination:
    """Pagination metadata returned by list endpoints."""

    page: int = 1
    per_page: int = 20
    total: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


@dataclass
class V2Meta:
    """Metadata wrapper from API v2 responses."""

    pagination: Optional[Pagination] = None
    request_id: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.pagination, dict):
            self.pagination = Pagination(**self.pagination)


@dataclass
class V2Error:
    """Error object from API v2 responses."""

    code: str = "UNKNOWN_ERROR"
    message: str = "An unknown error occurred"
    details: Optional[Dict[str, Any]] = None


@dataclass
class V2Response:
    """Top-level API v2 response envelope."""

    data: Any = None
    meta: Optional[V2Meta] = None
    error: Optional[V2Error] = None

    def __post_init__(self) -> None:
        if isinstance(self.meta, dict):
            self.meta = V2Meta(**self.meta)
        if isinstance(self.error, dict):
            self.error = V2Error(**self.error)


@dataclass
class Task:
    """Async task returned by long-running operations (create, rebuild, etc.)."""

    id: str = ""
    type: Optional[str] = None
    status: str = "pending"
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    progress: Optional[int] = None
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None

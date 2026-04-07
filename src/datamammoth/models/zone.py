"""Zone and image models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Zone:
    """A deployment zone / region."""

    id: str = ""
    name: Optional[str] = None
    slug: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    provider: Optional[str] = None
    status: str = "active"
    features: Optional[List[str]] = None
    available: bool = True


@dataclass
class Image:
    """An OS image available for server deployment."""

    id: str = ""
    name: Optional[str] = None
    slug: Optional[str] = None
    distribution: Optional[str] = None
    version: Optional[str] = None
    arch: Optional[str] = None
    min_disk_gb: Optional[int] = None
    type: Optional[str] = None
    zone_id: Optional[str] = None
    status: str = "active"
    created_at: Optional[str] = None

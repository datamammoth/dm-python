"""Server-related models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Server:
    """A provisioned server instance."""

    id: str = ""
    hostname: Optional[str] = None
    label: Optional[str] = None
    status: str = "unknown"
    ip_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    region: Optional[str] = None
    os_image: Optional[str] = None
    plan: Optional[str] = None
    product_id: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    provisioned_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Snapshot:
    """A server snapshot (backup image)."""

    id: str = ""
    server_id: Optional[str] = None
    name: Optional[str] = None
    status: str = "unknown"
    size_gb: Optional[float] = None
    created_at: Optional[str] = None


@dataclass
class Metric:
    """Server resource metrics (CPU, RAM, disk, bandwidth)."""

    timestamp: Optional[str] = None
    cpu_percent: Optional[float] = None
    ram_percent: Optional[float] = None
    disk_read_bps: Optional[float] = None
    disk_write_bps: Optional[float] = None
    net_in_bps: Optional[float] = None
    net_out_bps: Optional[float] = None


@dataclass
class ConsoleSession:
    """VNC/noVNC console session info."""

    url: str = ""
    token: Optional[str] = None
    type: str = "novnc"
    expires_at: Optional[str] = None


@dataclass
class FirewallRule:
    """A single firewall rule for a server."""

    id: Optional[str] = None
    direction: str = "inbound"
    protocol: str = "tcp"
    port_range: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    action: str = "allow"
    description: Optional[str] = None


@dataclass
class ServerEvent:
    """An event in a server's history (power on, reboot, etc.)."""

    id: str = ""
    server_id: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    initiated_by: Optional[str] = None
    created_at: Optional[str] = None

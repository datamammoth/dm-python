"""Tests for the DataMammoth sync client."""

import json

import httpx
import pytest
import respx

from datamammoth import DataMammoth
from datamammoth.exceptions import (
    AuthError,
    DataMammothError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from datamammoth.models.server import Server
from datamammoth.models.common import Task

BASE = "https://app.datamammoth.com/api/v2"


# ── Fixtures ────────────────────────────────────────────────────────────


@pytest.fixture
def dm():
    client = DataMammoth(api_key="dm_test_key_123")
    yield client
    client.close()


# ── Health ──────────────────────────────────────────────────────────────


@respx.mock
def test_health(dm):
    respx.get(f"{BASE}/health").mock(
        return_value=httpx.Response(200, json={"data": {"status": "ok", "version": "2.0.0"}})
    )
    result = dm.health()
    assert result["status"] == "ok"


# ── Servers ─────────────────────────────────────────────────────────────


@respx.mock
def test_list_servers(dm):
    respx.get(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "srv_001",
                        "hostname": "web-01",
                        "status": "active",
                        "ip_address": "1.2.3.4",
                        "created_at": "2026-01-01T00:00:00Z",
                    },
                    {
                        "id": "srv_002",
                        "hostname": "web-02",
                        "status": "active",
                        "ip_address": "5.6.7.8",
                        "created_at": "2026-01-02T00:00:00Z",
                    },
                ]
            },
        )
    )
    servers = dm.servers.list()
    assert len(servers) == 2
    assert isinstance(servers[0], Server)
    assert servers[0].id == "srv_001"
    assert servers[0].hostname == "web-01"
    assert servers[1].ip_address == "5.6.7.8"


@respx.mock
def test_get_server(dm):
    respx.get(f"{BASE}/servers/srv_001").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": {
                    "id": "srv_001",
                    "hostname": "web-01",
                    "status": "active",
                    "ip_address": "1.2.3.4",
                    "region": "eu-central",
                    "created_at": "2026-01-01T00:00:00Z",
                }
            },
        )
    )
    server = dm.servers.get("srv_001")
    assert server.hostname == "web-01"
    assert server.region == "eu-central"


@respx.mock
def test_create_server(dm):
    respx.post(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            202,
            json={
                "data": {
                    "id": "task_abc",
                    "type": "server.create",
                    "status": "pending",
                    "resource_id": "srv_003",
                    "resource_type": "server",
                }
            },
        )
    )
    task = dm.servers.create(product_id="prod_vps1", image_id="img_ubuntu2204", hostname="db-01")
    assert isinstance(task, Task)
    assert task.id == "task_abc"
    assert task.status == "pending"
    assert task.resource_id == "srv_003"


@respx.mock
def test_delete_server(dm):
    respx.delete(f"{BASE}/servers/srv_001").mock(
        return_value=httpx.Response(
            202,
            json={
                "data": {
                    "id": "task_del",
                    "type": "server.delete",
                    "status": "pending",
                }
            },
        )
    )
    task = dm.servers.delete("srv_001")
    assert task.id == "task_del"


@respx.mock
def test_power_on(dm):
    respx.post(f"{BASE}/servers/srv_001/actions/power-on").mock(
        return_value=httpx.Response(
            202,
            json={"data": {"id": "task_pw", "type": "server.power_on", "status": "pending"}},
        )
    )
    task = dm.servers.power_on("srv_001")
    assert task.type == "server.power_on"


@respx.mock
def test_snapshots(dm):
    respx.get(f"{BASE}/servers/srv_001/snapshots").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "snap_01", "name": "before-upgrade", "status": "available"},
                ]
            },
        )
    )
    snaps = dm.servers.snapshots("srv_001")
    assert len(snaps) == 1
    assert snaps[0].name == "before-upgrade"


@respx.mock
def test_firewall(dm):
    respx.get(f"{BASE}/servers/srv_001/firewall").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "fw_01",
                        "direction": "inbound",
                        "protocol": "tcp",
                        "port_range": "22",
                        "action": "allow",
                    }
                ]
            },
        )
    )
    rules = dm.servers.firewall("srv_001")
    assert len(rules) == 1
    assert rules[0].port_range == "22"


# ── Products ────────────────────────────────────────────────────────────


@respx.mock
def test_list_products(dm):
    respx.get(f"{BASE}/products").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prod_vps1",
                        "name": "VPS S",
                        "status": "active",
                        "pricing": {"monthly": 5.99, "currency": "USD"},
                    }
                ]
            },
        )
    )
    products = dm.products.list()
    assert len(products) == 1
    assert products[0].pricing.monthly == 5.99


@respx.mock
def test_categories(dm):
    respx.get(f"{BASE}/categories").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "cat_1", "name": "VPS", "slug": "vps"}]},
        )
    )
    cats = dm.products.categories()
    assert cats[0].slug == "vps"


# ── Billing ─────────────────────────────────────────────────────────────


@respx.mock
def test_invoices(dm):
    respx.get(f"{BASE}/invoices").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "inv_001", "status": "paid", "total": 29.99, "currency": "USD"}
                ]
            },
        )
    )
    invoices = dm.billing.invoices()
    assert invoices[0].total == 29.99


@respx.mock
def test_balance(dm):
    respx.get(f"{BASE}/balance").mock(
        return_value=httpx.Response(
            200,
            json={"data": {"amount": 150.00, "currency": "USD"}},
        )
    )
    bal = dm.billing.balance()
    assert bal.amount == 150.00


# ── Support ─────────────────────────────────────────────────────────────


@respx.mock
def test_create_ticket(dm):
    respx.post(f"{BASE}/tickets").mock(
        return_value=httpx.Response(
            201,
            json={
                "data": {
                    "id": "tkt_001",
                    "subject": "Help please",
                    "status": "open",
                    "priority": "medium",
                }
            },
        )
    )
    ticket = dm.support.create_ticket(subject="Help please", body="I need help with...")
    assert ticket.id == "tkt_001"
    assert ticket.status == "open"


# ── Account ─────────────────────────────────────────────────────────────


@respx.mock
def test_me(dm):
    respx.get(f"{BASE}/me").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": {
                    "id": "usr_001",
                    "email": "user@example.com",
                    "name": "Test User",
                }
            },
        )
    )
    profile = dm.account.me()
    assert profile.email == "user@example.com"


@respx.mock
def test_api_keys(dm):
    respx.get(f"{BASE}/me/api-keys").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "key_001", "name": "CI Key", "key_prefix": "dm_ci_"}
                ]
            },
        )
    )
    keys = dm.account.api_keys()
    assert len(keys) == 1
    assert keys[0].name == "CI Key"


# ── Webhooks ────────────────────────────────────────────────────────────


@respx.mock
def test_create_webhook(dm):
    respx.post(f"{BASE}/webhooks").mock(
        return_value=httpx.Response(
            201,
            json={
                "data": {
                    "id": "wh_001",
                    "url": "https://example.com/hook",
                    "events": ["server.created"],
                    "is_active": True,
                }
            },
        )
    )
    wh = dm.webhooks.create(url="https://example.com/hook", events=["server.created"])
    assert wh.id == "wh_001"
    assert wh.events == ["server.created"]


@respx.mock
def test_event_types(dm):
    respx.get(f"{BASE}/webhooks/events").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"name": "server.created", "category": "server"},
                    {"name": "invoice.paid", "category": "billing"},
                ]
            },
        )
    )
    events = dm.webhooks.event_types()
    assert len(events) == 2


# ── Zones ───────────────────────────────────────────────────────────────


@respx.mock
def test_list_zones(dm):
    respx.get(f"{BASE}/zones").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "zone_eu1", "name": "EU Central", "slug": "eu-central"}
                ]
            },
        )
    )
    zones = dm.zones.list()
    assert zones[0].slug == "eu-central"


@respx.mock
def test_zone_images(dm):
    respx.get(f"{BASE}/zones/zone_eu1/images").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "img_001",
                        "name": "Ubuntu 22.04",
                        "distribution": "ubuntu",
                    }
                ]
            },
        )
    )
    images = dm.zones.images("zone_eu1")
    assert images[0].distribution == "ubuntu"


# ── Error Handling ──────────────────────────────────────────────────────


@respx.mock
def test_401_raises_auth_error(dm):
    respx.get(f"{BASE}/me").mock(
        return_value=httpx.Response(
            401,
            json={"error": {"code": "INVALID_API_KEY", "message": "Invalid API key"}},
        )
    )
    with pytest.raises(AuthError) as exc:
        dm.account.me()
    assert exc.value.status == 401
    assert "INVALID_API_KEY" in str(exc.value)


@respx.mock
def test_404_raises_not_found(dm):
    respx.get(f"{BASE}/servers/srv_nonexistent").mock(
        return_value=httpx.Response(
            404,
            json={"error": {"code": "NOT_FOUND", "message": "Server not found"}},
        )
    )
    with pytest.raises(NotFoundError):
        dm.servers.get("srv_nonexistent")


@respx.mock
def test_422_raises_validation_error(dm):
    respx.post(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            422,
            json={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": {
                        "errors": {"product_id": "Product ID is required"}
                    },
                }
            },
        )
    )
    with pytest.raises(ValidationError) as exc:
        dm.servers.create(product_id="", image_id="img_001")
    assert "product_id" in exc.value.field_errors


@respx.mock
def test_429_raises_rate_limit(dm):
    respx.get(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            429,
            json={"error": {"code": "RATE_LIMITED", "message": "Too many requests"}},
            headers={"Retry-After": "5"},
        )
    )
    with pytest.raises(RateLimitError) as exc:
        dm.servers.list()
    assert exc.value.retry_after == 5


@respx.mock
def test_204_returns_none(dm):
    respx.delete(f"{BASE}/me/api-keys/key_001").mock(
        return_value=httpx.Response(204)
    )
    result = dm.account.delete_api_key("key_001")
    assert result is None


# ── Context Manager ─────────────────────────────────────────────────────


@respx.mock
def test_context_manager():
    respx.get(f"{BASE}/health").mock(
        return_value=httpx.Response(200, json={"data": {"status": "ok"}})
    )
    with DataMammoth(api_key="dm_test") as dm:
        result = dm.health()
        assert result["status"] == "ok"


# ── Pagination ──────────────────────────────────────────────────────────


@respx.mock
def test_pagination_iterator(dm):
    # Page 1
    respx.get(f"{BASE}/servers").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "data": [{"id": "srv_001", "status": "active"}],
                    "meta": {"pagination": {"page": 1, "has_next": True}},
                },
            ),
            httpx.Response(
                200,
                json={
                    "data": [{"id": "srv_002", "status": "active"}],
                    "meta": {"pagination": {"page": 2, "has_next": False}},
                },
            ),
        ]
    )
    all_servers = list(dm.servers.list_all())
    assert len(all_servers) == 2
    assert all_servers[0].id == "srv_001"
    assert all_servers[1].id == "srv_002"


# ── Repr ────────────────────────────────────────────────────────────────


def test_repr(dm):
    assert "datamammoth.com" in repr(dm)

"""Tests for the DataMammoth async client."""

import httpx
import pytest
import respx

from datamammoth import AsyncDataMammoth
from datamammoth.exceptions import AuthError
from datamammoth.models.server import Server

BASE = "https://app.datamammoth.com/api/v2"


@pytest.fixture
async def dm():
    client = AsyncDataMammoth(api_key="dm_test_key_123")
    yield client
    await client.close()


@respx.mock
@pytest.mark.asyncio
async def test_async_health():
    respx.get(f"{BASE}/health").mock(
        return_value=httpx.Response(200, json={"data": {"status": "ok"}})
    )
    async with AsyncDataMammoth(api_key="dm_test") as dm:
        result = await dm.health()
        assert result["status"] == "ok"


@respx.mock
@pytest.mark.asyncio
async def test_async_list_servers():
    respx.get(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "srv_001", "hostname": "web-01", "status": "active"},
                ]
            },
        )
    )
    async with AsyncDataMammoth(api_key="dm_test") as dm:
        servers = await dm.servers.list()
        assert len(servers) == 1
        assert isinstance(servers[0], Server)
        assert servers[0].hostname == "web-01"


@respx.mock
@pytest.mark.asyncio
async def test_async_get_server():
    respx.get(f"{BASE}/servers/srv_001").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": {
                    "id": "srv_001",
                    "hostname": "web-01",
                    "status": "active",
                    "ip_address": "1.2.3.4",
                }
            },
        )
    )
    async with AsyncDataMammoth(api_key="dm_test") as dm:
        server = await dm.servers.get("srv_001")
        assert server.ip_address == "1.2.3.4"


@respx.mock
@pytest.mark.asyncio
async def test_async_auth_error():
    respx.get(f"{BASE}/me").mock(
        return_value=httpx.Response(
            401,
            json={"error": {"code": "INVALID_API_KEY", "message": "Invalid API key"}},
        )
    )
    async with AsyncDataMammoth(api_key="dm_bad") as dm:
        with pytest.raises(AuthError):
            await dm.account.me()


@respx.mock
@pytest.mark.asyncio
async def test_async_create_server():
    respx.post(f"{BASE}/servers").mock(
        return_value=httpx.Response(
            202,
            json={
                "data": {
                    "id": "task_abc",
                    "type": "server.create",
                    "status": "pending",
                    "resource_id": "srv_003",
                }
            },
        )
    )
    async with AsyncDataMammoth(api_key="dm_test") as dm:
        task = await dm.servers.create(product_id="prod_1", image_id="img_1")
        assert task.resource_id == "srv_003"


@respx.mock
@pytest.mark.asyncio
async def test_async_pagination():
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
    async with AsyncDataMammoth(api_key="dm_test") as dm:
        all_servers = await dm.servers.list_all().to_list()
        assert len(all_servers) == 2

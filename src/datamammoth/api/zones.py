"""Zones API — deployment regions and OS images."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth.models.zone import Image, Zone


class ZonesAPI:
    """Synchronous zones API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    def list(self) -> List[Zone]:
        """List all available deployment zones."""
        data = self._client.get("/zones")
        return [Zone(**z) for z in data]

    def images(
        self,
        zone_id: str,
        filter_distribution: Optional[str] = None,
        filter_type: Optional[str] = None,
    ) -> List[Image]:
        """List OS images available in a zone."""
        params: Dict[str, Any] = {}
        if filter_distribution:
            params["filter[distribution]"] = filter_distribution
        if filter_type:
            params["filter[type]"] = filter_type
        data = self._client.get(f"/zones/{zone_id}/images", params=params)
        return [Image(**i) for i in data]


class AsyncZonesAPI:
    """Asynchronous zones API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def list(self) -> List[Zone]:
        data = await self._client.get("/zones")
        return [Zone(**z) for z in data]

    async def images(
        self,
        zone_id: str,
        filter_distribution: Optional[str] = None,
        filter_type: Optional[str] = None,
    ) -> List[Image]:
        params: Dict[str, Any] = {}
        if filter_distribution:
            params["filter[distribution]"] = filter_distribution
        if filter_type:
            params["filter[type]"] = filter_type
        data = await self._client.get(f"/zones/{zone_id}/images", params=params)
        return [Image(**i) for i in data]

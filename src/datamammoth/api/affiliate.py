"""Affiliate API — affiliate profile, commissions, referrals, payouts, materials."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.affiliate import (
    Affiliate,
    Commission,
    Material,
    Payout,
    Referral,
)


class AffiliateAPI:
    """Synchronous affiliate API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Affiliate Profile ────────────────────────────────────────────

    def me(self) -> Affiliate:
        """Get the current user's affiliate profile."""
        return Affiliate(**self._client.get("/affiliate/me"))

    def update_profile(self, **fields: Any) -> Affiliate:
        """Update affiliate profile settings."""
        return Affiliate(**self._client.patch("/affiliate/me", json=fields))

    # ── Commissions ──────────────────────────────────────────────────

    def commissions(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Commission]:
        """List earned commissions."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/affiliate/commissions", params=params)
        return [Commission(**c) for c in data]

    def commissions_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all commissions."""
        return PageIterator(
            self._client, "/affiliate/commissions", params=kwargs, model=Commission
        )

    # ── Referrals ────────────────────────────────────────────────────

    def referrals(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Referral]:
        """List referrals."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/affiliate/referrals", params=params)
        return [Referral(**r) for r in data]

    def referrals_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all referrals."""
        return PageIterator(
            self._client, "/affiliate/referrals", params=kwargs, model=Referral
        )

    # ── Payouts ──────────────────────────────────────────────────────

    def request_payout(
        self,
        amount: float,
        method: str,
        notes: Optional[str] = None,
    ) -> Payout:
        """Request a payout."""
        body: Dict[str, Any] = {"amount": amount, "method": method}
        if notes:
            body["notes"] = notes
        return Payout(**self._client.post("/affiliate/payout-request", json=body))

    # ── Marketing Materials ──────────────────────────────────────────

    def materials(
        self,
        page: int = 1,
        per_page: int = 20,
        filter_type: Optional[str] = None,
    ) -> List[Material]:
        """List available marketing materials (banners, links, etc.)."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if filter_type:
            params["filter[type]"] = filter_type
        data = self._client.get("/affiliate/materials", params=params)
        return [Material(**m) for m in data]


class AsyncAffiliateAPI:
    """Asynchronous affiliate API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def me(self) -> Affiliate:
        return Affiliate(**await self._client.get("/affiliate/me"))

    async def update_profile(self, **fields: Any) -> Affiliate:
        return Affiliate(**await self._client.patch("/affiliate/me", json=fields))

    async def commissions(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Commission]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/affiliate/commissions", params=params)
        return [Commission(**c) for c in data]

    def commissions_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(
            self._client, "/affiliate/commissions", params=kwargs, model=Commission
        )

    async def referrals(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Referral]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/affiliate/referrals", params=params)
        return [Referral(**r) for r in data]

    def referrals_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(
            self._client, "/affiliate/referrals", params=kwargs, model=Referral
        )

    async def request_payout(
        self, amount: float, method: str, notes: Optional[str] = None
    ) -> Payout:
        body: Dict[str, Any] = {"amount": amount, "method": method}
        if notes:
            body["notes"] = notes
        return Payout(**await self._client.post("/affiliate/payout-request", json=body))

    async def materials(
        self,
        page: int = 1,
        per_page: int = 20,
        filter_type: Optional[str] = None,
    ) -> List[Material]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if filter_type:
            params["filter[type]"] = filter_type
        data = await self._client.get("/affiliate/materials", params=params)
        return [Material(**m) for m in data]

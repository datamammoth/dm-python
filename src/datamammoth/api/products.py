"""Products API — browse catalog, options, addons, and pricing."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.product import (
    Category,
    Product,
    ProductAddon,
    ProductOption,
    ProductPricing,
)


class ProductsAPI:
    """Synchronous products API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Products ─────────────────────────────────────────────────────

    def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "name",
        search: Optional[str] = None,
        filter_category: Optional[str] = None,
        filter_type: Optional[str] = None,
        filter_status: Optional[str] = None,
    ) -> List[Product]:
        """List available products."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_category:
            params["filter[category]"] = filter_category
        if filter_type:
            params["filter[type]"] = filter_type
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/products", params=params)
        return [Product(**p) for p in data]

    def list_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all products."""
        return PageIterator(self._client, "/products", params=kwargs, model=Product)

    def get(self, product_id: str) -> Product:
        """Get a single product by ID."""
        return Product(**self._client.get(f"/products/{product_id}"))

    # ── Options ──────────────────────────────────────────────────────

    def options(self, product_id: str) -> List[ProductOption]:
        """List configurable options for a product."""
        data = self._client.get(f"/products/{product_id}/options")
        return [ProductOption(**o) for o in data]

    # ── Addons ───────────────────────────────────────────────────────

    def addons(self, product_id: str) -> List[ProductAddon]:
        """List available addons for a product."""
        data = self._client.get(f"/products/{product_id}/addons")
        return [ProductAddon(**a) for a in data]

    # ── Pricing ──────────────────────────────────────────────────────

    def pricing(self, product_id: str) -> ProductPricing:
        """Get pricing for a product."""
        return ProductPricing(**self._client.get(f"/products/{product_id}/pricing"))

    # ── Categories ───────────────────────────────────────────────────

    def categories(self) -> List[Category]:
        """List all product categories."""
        data = self._client.get("/categories")
        return [Category(**c) for c in data]

    # ── Promo code validation ────────────────────────────────────────

    def validate_promo(self, code: str, product_id: Optional[str] = None) -> dict:
        """Validate a promotional code."""
        body: Dict[str, Any] = {"code": code}
        if product_id:
            body["product_id"] = product_id
        return self._client.post("/promo/validate", json=body)


class AsyncProductsAPI:
    """Asynchronous products API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def list(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "name",
        search: Optional[str] = None,
        filter_category: Optional[str] = None,
        filter_type: Optional[str] = None,
        filter_status: Optional[str] = None,
    ) -> List[Product]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if search:
            params["search"] = search
        if filter_category:
            params["filter[category]"] = filter_category
        if filter_type:
            params["filter[type]"] = filter_type
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/products", params=params)
        return [Product(**p) for p in data]

    def list_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/products", params=kwargs, model=Product)

    async def get(self, product_id: str) -> Product:
        return Product(**await self._client.get(f"/products/{product_id}"))

    async def options(self, product_id: str) -> List[ProductOption]:
        data = await self._client.get(f"/products/{product_id}/options")
        return [ProductOption(**o) for o in data]

    async def addons(self, product_id: str) -> List[ProductAddon]:
        data = await self._client.get(f"/products/{product_id}/addons")
        return [ProductAddon(**a) for a in data]

    async def pricing(self, product_id: str) -> ProductPricing:
        return ProductPricing(**await self._client.get(f"/products/{product_id}/pricing"))

    async def categories(self) -> List[Category]:
        data = await self._client.get("/categories")
        return [Category(**c) for c in data]

    async def validate_promo(self, code: str, product_id: Optional[str] = None) -> dict:
        body: Dict[str, Any] = {"code": code}
        if product_id:
            body["product_id"] = product_id
        return await self._client.post("/promo/validate", json=body)

"""Billing API — invoices, subscriptions, balance, payments, orders."""

from typing import Any, Dict, List, Optional

from datamammoth._base import _BaseClient, _AsyncBaseClient
from datamammoth._pagination import PageIterator, AsyncPageIterator
from datamammoth.models.billing import (
    Balance,
    Invoice,
    Order,
    PaymentMethod,
    Subscription,
    Transaction,
)


class BillingAPI:
    """Synchronous billing API."""

    def __init__(self, client: _BaseClient):
        self._client = client

    # ── Invoices ─────────────────────────────────────────────────────

    def invoices(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Invoice]:
        """List invoices."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/invoices", params=params)
        return [Invoice(**i) for i in data]

    def invoices_all(self, **kwargs: Any) -> PageIterator:
        """Auto-paginate through all invoices."""
        return PageIterator(self._client, "/invoices", params=kwargs, model=Invoice)

    def get_invoice(self, invoice_id: str) -> Invoice:
        """Get a single invoice."""
        return Invoice(**self._client.get(f"/invoices/{invoice_id}"))

    def pay_invoice(self, invoice_id: str, payment_method_id: Optional[str] = None) -> dict:
        """Pay an invoice."""
        body: Dict[str, Any] = {}
        if payment_method_id:
            body["payment_method_id"] = payment_method_id
        return self._client.post(f"/invoices/{invoice_id}/pay", json=body)

    # ── Subscriptions ────────────────────────────────────────────────

    def subscriptions(
        self,
        page: int = 1,
        per_page: int = 20,
        filter_status: Optional[str] = None,
    ) -> List[Subscription]:
        """List subscriptions."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if filter_status:
            params["filter[status]"] = filter_status
        data = self._client.get("/subscriptions", params=params)
        return [Subscription(**s) for s in data]

    def get_subscription(self, subscription_id: str) -> Subscription:
        """Get a single subscription."""
        return Subscription(**self._client.get(f"/subscriptions/{subscription_id}"))

    def cancel_subscription(self, subscription_id: str, immediate: bool = False) -> Subscription:
        """Cancel a subscription."""
        return Subscription(
            **self._client.patch(
                f"/subscriptions/{subscription_id}",
                json={"status": "cancelled", "immediate": immediate},
            )
        )

    # ── Balance / Transactions ───────────────────────────────────────

    def balance(self) -> Balance:
        """Get the account credit balance."""
        return Balance(**self._client.get("/balance"))

    def transactions(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
    ) -> List[Transaction]:
        """List balance transactions."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        data = self._client.get("/balance/transactions", params=params)
        return [Transaction(**t) for t in data]

    # ── Payment Methods ──────────────────────────────────────────────

    def payment_methods(self) -> List[PaymentMethod]:
        """List stored payment methods."""
        data = self._client.get("/payment-methods")
        return [PaymentMethod(**pm) for pm in data]

    # ── Orders ───────────────────────────────────────────────────────

    def orders(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
    ) -> List[Order]:
        """List orders."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        data = self._client.get("/orders", params=params)
        return [Order(**o) for o in data]

    def get_order(self, order_id: str) -> Order:
        """Get a single order."""
        return Order(**self._client.get(f"/orders/{order_id}"))


class AsyncBillingAPI:
    """Asynchronous billing API."""

    def __init__(self, client: _AsyncBaseClient):
        self._client = client

    async def invoices(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
        filter_status: Optional[str] = None,
    ) -> List[Invoice]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/invoices", params=params)
        return [Invoice(**i) for i in data]

    def invoices_all(self, **kwargs: Any) -> AsyncPageIterator:
        return AsyncPageIterator(self._client, "/invoices", params=kwargs, model=Invoice)

    async def get_invoice(self, invoice_id: str) -> Invoice:
        return Invoice(**await self._client.get(f"/invoices/{invoice_id}"))

    async def pay_invoice(self, invoice_id: str, payment_method_id: Optional[str] = None) -> dict:
        body: Dict[str, Any] = {}
        if payment_method_id:
            body["payment_method_id"] = payment_method_id
        return await self._client.post(f"/invoices/{invoice_id}/pay", json=body)

    async def subscriptions(
        self,
        page: int = 1,
        per_page: int = 20,
        filter_status: Optional[str] = None,
    ) -> List[Subscription]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if filter_status:
            params["filter[status]"] = filter_status
        data = await self._client.get("/subscriptions", params=params)
        return [Subscription(**s) for s in data]

    async def get_subscription(self, subscription_id: str) -> Subscription:
        return Subscription(**await self._client.get(f"/subscriptions/{subscription_id}"))

    async def cancel_subscription(
        self, subscription_id: str, immediate: bool = False
    ) -> Subscription:
        return Subscription(
            **await self._client.patch(
                f"/subscriptions/{subscription_id}",
                json={"status": "cancelled", "immediate": immediate},
            )
        )

    async def balance(self) -> Balance:
        return Balance(**await self._client.get("/balance"))

    async def transactions(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
    ) -> List[Transaction]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        data = await self._client.get("/balance/transactions", params=params)
        return [Transaction(**t) for t in data]

    async def payment_methods(self) -> List[PaymentMethod]:
        data = await self._client.get("/payment-methods")
        return [PaymentMethod(**pm) for pm in data]

    async def orders(
        self,
        page: int = 1,
        per_page: int = 20,
        sort: str = "-created_at",
    ) -> List[Order]:
        params: Dict[str, Any] = {"page": page, "per_page": per_page, "sort": sort}
        data = await self._client.get("/orders", params=params)
        return [Order(**o) for o in data]

    async def get_order(self, order_id: str) -> Order:
        return Order(**await self._client.get(f"/orders/{order_id}"))

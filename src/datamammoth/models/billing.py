"""Billing, invoice, and payment models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class InvoiceItem:
    """A line item on an invoice."""

    id: Optional[str] = None
    description: Optional[str] = None
    quantity: int = 1
    unit_price: Optional[float] = None
    total: Optional[float] = None
    product_id: Optional[str] = None


@dataclass
class Invoice:
    """A billing invoice."""

    id: str = ""
    number: Optional[str] = None
    status: str = "draft"
    currency: str = "USD"
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    amount_paid: Optional[float] = None
    amount_due: Optional[float] = None
    items: Optional[List[InvoiceItem]] = None
    due_date: Optional[str] = None
    paid_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self) -> None:
        if self.items and isinstance(self.items, list):
            self.items = [
                InvoiceItem(**i) if isinstance(i, dict) else i for i in self.items
            ]


@dataclass
class Subscription:
    """A recurring subscription."""

    id: str = ""
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    status: str = "active"
    billing_cycle: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "USD"
    next_due_date: Optional[str] = None
    server_id: Optional[str] = None
    auto_renew: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Balance:
    """Account credit balance."""

    amount: float = 0.0
    currency: str = "USD"
    updated_at: Optional[str] = None


@dataclass
class Transaction:
    """A balance transaction (credit/debit)."""

    id: str = ""
    type: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "USD"
    description: Optional[str] = None
    balance_after: Optional[float] = None
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class PaymentMethod:
    """A stored payment method."""

    id: str = ""
    type: Optional[str] = None
    label: Optional[str] = None
    is_default: bool = False
    last_four: Optional[str] = None
    brand: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    created_at: Optional[str] = None


@dataclass
class Order:
    """A product order."""

    id: str = ""
    status: str = "pending"
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    total: Optional[float] = None
    currency: str = "USD"
    promo_code: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    invoice_id: Optional[str] = None
    server_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

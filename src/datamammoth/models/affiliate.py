"""Affiliate program models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Affiliate:
    """An affiliate account."""

    id: str = ""
    user_id: Optional[str] = None
    status: str = "active"
    referral_code: Optional[str] = None
    referral_url: Optional[str] = None
    commission_rate: Optional[float] = None
    commission_type: Optional[str] = None
    total_earned: Optional[float] = None
    total_paid: Optional[float] = None
    pending_balance: Optional[float] = None
    referral_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Commission:
    """A commission earned from a referral."""

    id: str = ""
    affiliate_id: Optional[str] = None
    referral_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "USD"
    status: str = "pending"
    type: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Referral:
    """A referred user/signup."""

    id: str = ""
    affiliate_id: Optional[str] = None
    referred_user_id: Optional[str] = None
    referred_email: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    total_revenue: Optional[float] = None
    total_commissions: Optional[float] = None
    signed_up_at: Optional[str] = None
    first_order_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Payout:
    """An affiliate payout request."""

    id: str = ""
    affiliate_id: Optional[str] = None
    amount: Optional[float] = None
    currency: str = "USD"
    method: Optional[str] = None
    status: str = "pending"
    reference: Optional[str] = None
    notes: Optional[str] = None
    requested_at: Optional[str] = None
    processed_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Material:
    """Affiliate marketing material (banner, link, etc.)."""

    id: str = ""
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    dimensions: Optional[str] = None
    clicks: int = 0
    created_at: Optional[str] = None

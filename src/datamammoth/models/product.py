"""Product, addon, and category models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ProductPricing:
    """Pricing information for a product."""

    monthly: Optional[float] = None
    quarterly: Optional[float] = None
    semi_annual: Optional[float] = None
    annual: Optional[float] = None
    currency: str = "USD"
    setup_fee: Optional[float] = None


@dataclass
class ProductOption:
    """A configurable option for a product (e.g. extra RAM, storage)."""

    id: str = ""
    name: Optional[str] = None
    label: Optional[str] = None
    type: str = "select"
    required: bool = False
    choices: Optional[List[Dict[str, Any]]] = None
    default_value: Optional[str] = None


@dataclass
class ProductAddon:
    """An addon that can be attached to a product."""

    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    pricing: Optional[ProductPricing] = None
    category: Optional[str] = None
    group_id: Optional[int] = None

    def __post_init__(self) -> None:
        if isinstance(self.pricing, dict):
            self.pricing = ProductPricing(**self.pricing)


@dataclass
class Product:
    """A hosting product (VPS plan, dedicated server, etc.)."""

    id: str = ""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    type: Optional[str] = None
    status: str = "active"
    specs: Optional[Dict[str, Any]] = None
    pricing: Optional[ProductPricing] = None
    options: Optional[List[ProductOption]] = None
    addons: Optional[List[ProductAddon]] = None
    region: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.pricing, dict):
            self.pricing = ProductPricing(**self.pricing)
        if self.options and isinstance(self.options, list):
            self.options = [
                ProductOption(**o) if isinstance(o, dict) else o for o in self.options
            ]
        if self.addons and isinstance(self.addons, list):
            self.addons = [
                ProductAddon(**a) if isinstance(a, dict) else a for a in self.addons
            ]


@dataclass
class Category:
    """A product category."""

    id: str = ""
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[str] = None
    sort_order: int = 0
    product_count: int = 0

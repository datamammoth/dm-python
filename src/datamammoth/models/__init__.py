"""DataMammoth data models — lightweight dataclasses for all API resources."""

from datamammoth.models.common import (
    V2Response,
    V2Meta,
    V2Error,
    Pagination,
    Task,
)
from datamammoth.models.server import (
    Server,
    Snapshot,
    Metric,
    ConsoleSession,
    FirewallRule,
    ServerEvent,
)
from datamammoth.models.product import (
    Product,
    ProductOption,
    ProductAddon,
    ProductPricing,
    Category,
)
from datamammoth.models.billing import (
    Invoice,
    InvoiceItem,
    Subscription,
    Balance,
    Transaction,
    PaymentMethod,
    Order,
)
from datamammoth.models.support import (
    Ticket,
    TicketReply,
    Department,
    KBArticle,
    TicketFeedback,
)
from datamammoth.models.account import (
    UserProfile,
    ApiKey,
    Session,
    Notification,
    Activity,
    TwoFactorStatus,
)
from datamammoth.models.admin import (
    AdminUser,
    Role,
    Tenant,
    Lead,
    AuditLogEntry,
    DashboardStats,
)
from datamammoth.models.affiliate import (
    Affiliate,
    Commission,
    Referral,
    Payout,
    Material,
)
from datamammoth.models.webhook import (
    Webhook,
    WebhookDelivery,
    EventType,
)
from datamammoth.models.zone import (
    Zone,
    Image,
)

__all__ = [
    "V2Response",
    "V2Meta",
    "V2Error",
    "Pagination",
    "Task",
    "Server",
    "Snapshot",
    "Metric",
    "ConsoleSession",
    "FirewallRule",
    "ServerEvent",
    "Product",
    "ProductOption",
    "ProductAddon",
    "ProductPricing",
    "Category",
    "Invoice",
    "InvoiceItem",
    "Subscription",
    "Balance",
    "Transaction",
    "PaymentMethod",
    "Order",
    "Ticket",
    "TicketReply",
    "Department",
    "KBArticle",
    "TicketFeedback",
    "Affiliate",
    "Commission",
    "Referral",
    "Payout",
    "Material",
    "UserProfile",
    "ApiKey",
    "Session",
    "Notification",
    "Activity",
    "TwoFactorStatus",
    "AdminUser",
    "Role",
    "Tenant",
    "Lead",
    "AuditLogEntry",
    "DashboardStats",
    "Webhook",
    "WebhookDelivery",
    "EventType",
    "Zone",
    "Image",
]

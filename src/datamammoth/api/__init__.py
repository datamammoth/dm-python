"""API resource classes — one per domain."""

from datamammoth.api.servers import ServersAPI, AsyncServersAPI
from datamammoth.api.products import ProductsAPI, AsyncProductsAPI
from datamammoth.api.billing import BillingAPI, AsyncBillingAPI
from datamammoth.api.support import SupportAPI, AsyncSupportAPI
from datamammoth.api.account import AccountAPI, AsyncAccountAPI
from datamammoth.api.admin import AdminAPI, AsyncAdminAPI
from datamammoth.api.affiliate import AffiliateAPI, AsyncAffiliateAPI
from datamammoth.api.webhooks import WebhooksAPI, AsyncWebhooksAPI
from datamammoth.api.tasks import TasksAPI, AsyncTasksAPI
from datamammoth.api.zones import ZonesAPI, AsyncZonesAPI

__all__ = [
    "ServersAPI",
    "AsyncServersAPI",
    "ProductsAPI",
    "AsyncProductsAPI",
    "BillingAPI",
    "AsyncBillingAPI",
    "SupportAPI",
    "AsyncSupportAPI",
    "AccountAPI",
    "AsyncAccountAPI",
    "AdminAPI",
    "AsyncAdminAPI",
    "AffiliateAPI",
    "AsyncAffiliateAPI",
    "WebhooksAPI",
    "AsyncWebhooksAPI",
    "TasksAPI",
    "AsyncTasksAPI",
    "ZonesAPI",
    "AsyncZonesAPI",
]

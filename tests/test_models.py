"""Tests for model dataclasses."""

from datamammoth.models.server import Server, Snapshot, FirewallRule
from datamammoth.models.product import Product, ProductPricing, ProductOption, ProductAddon
from datamammoth.models.billing import Invoice, InvoiceItem, Subscription, Balance
from datamammoth.models.support import Ticket, TicketReply
from datamammoth.models.account import UserProfile, ApiKey
from datamammoth.models.admin import AdminUser, Role, DashboardStats
from datamammoth.models.affiliate import Affiliate, Commission
from datamammoth.models.webhook import Webhook, EventType
from datamammoth.models.zone import Zone, Image
from datamammoth.models.common import Task, V2Response, V2Meta, Pagination


def test_server_from_dict():
    s = Server(
        id="srv_001",
        hostname="web-01",
        status="active",
        ip_address="1.2.3.4",
        specs={"vcpu": 4, "ram_gb": 8},
    )
    assert s.id == "srv_001"
    assert s.specs["vcpu"] == 4


def test_server_defaults():
    s = Server()
    assert s.id == ""
    assert s.status == "unknown"
    assert s.hostname is None


def test_product_nested_pricing():
    p = Product(
        id="prod_1",
        name="VPS S",
        pricing={"monthly": 5.99, "currency": "USD"},
    )
    assert isinstance(p.pricing, ProductPricing)
    assert p.pricing.monthly == 5.99


def test_product_nested_options_and_addons():
    p = Product(
        id="prod_1",
        options=[{"id": "opt_1", "name": "Extra RAM", "type": "select"}],
        addons=[{"id": "add_1", "name": "Backup", "pricing": {"monthly": 2.0}}],
    )
    assert isinstance(p.options[0], ProductOption)
    assert isinstance(p.addons[0], ProductAddon)
    assert isinstance(p.addons[0].pricing, ProductPricing)


def test_invoice_with_items():
    inv = Invoice(
        id="inv_001",
        items=[
            {"id": "li_1", "description": "VPS S", "total": 5.99},
        ],
    )
    assert isinstance(inv.items[0], InvoiceItem)
    assert inv.items[0].total == 5.99


def test_ticket_with_replies():
    t = Ticket(
        id="tkt_001",
        subject="Help",
        replies=[{"id": "rep_1", "body": "Thanks for reaching out"}],
    )
    assert isinstance(t.replies[0], TicketReply)


def test_task_defaults():
    t = Task()
    assert t.status == "pending"
    assert t.id == ""


def test_v2response_nested():
    r = V2Response(
        data={"hello": "world"},
        meta={"pagination": {"page": 1, "total": 100, "has_next": True}},
    )
    assert isinstance(r.meta, V2Meta)
    assert isinstance(r.meta.pagination, Pagination)
    assert r.meta.pagination.has_next is True


def test_dashboard_stats():
    stats = DashboardStats(total_users=500, active_servers=120, mrr=8500.50)
    assert stats.mrr == 8500.50


def test_zone():
    z = Zone(id="zone_1", name="EU Central", slug="eu-central", country="DE")
    assert z.country == "DE"


def test_image():
    i = Image(id="img_1", name="Ubuntu 22.04", distribution="ubuntu", version="22.04")
    assert i.version == "22.04"


def test_webhook():
    w = Webhook(id="wh_1", url="https://example.com/hook", events=["server.created"])
    assert w.events == ["server.created"]


def test_affiliate():
    a = Affiliate(id="aff_1", referral_code="ABC123", total_earned=500.0)
    assert a.referral_code == "ABC123"

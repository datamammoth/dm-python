#!/usr/bin/env python3
"""Example: Register a webhook and list available event types.

This example shows how to register a webhook endpoint and explore
the available event types. For a real webhook listener, you'd use
a web framework like Flask or FastAPI to receive the payloads.
"""

import os

from datamammoth import DataMammoth

api_key = os.environ.get("DM_API_KEY", "dm_your_key_here")

dm = DataMammoth(api_key=api_key)

# 1. List available event types
events = dm.webhooks.event_types()
print("Available webhook events:")
for evt in events:
    print(f"  {evt.name} ({evt.category or 'general'})")
    if evt.description:
        print(f"    {evt.description}")
print()

# 2. Register a webhook
webhook = dm.webhooks.create(
    url="https://your-app.example.com/webhooks/datamammoth",
    events=["server.created", "server.deleted", "invoice.paid"],
    description="Production webhook",
    secret="whsec_your_signing_secret",
)
print(f"Webhook registered: {webhook.id}")
print(f"  URL:    {webhook.url}")
print(f"  Events: {webhook.events}")
print()

# 3. Send a test delivery
print("Sending test payload...")
delivery = dm.webhooks.test(webhook.id)
print(f"  Delivery ID: {delivery.id}")
print(f"  Status:      {delivery.response_status}")
print(f"  Success:     {delivery.success}")
print()

# 4. List existing webhooks
webhooks = dm.webhooks.list()
print(f"Total webhooks: {len(webhooks)}")
for wh in webhooks:
    status = "active" if wh.is_active else "inactive"
    print(f"  {wh.id}: {wh.url} [{status}]")

dm.close()

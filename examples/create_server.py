#!/usr/bin/env python3
"""Example: Create a new server and wait for provisioning to complete."""

import os

from datamammoth import DataMammoth

api_key = os.environ.get("DM_API_KEY", "dm_your_key_here")

dm = DataMammoth(api_key=api_key)

# 1. Browse available zones and images
zones = dm.zones.list()
print("Available zones:")
for zone in zones:
    print(f"  {zone.id}: {zone.name} ({zone.country})")

# Pick a zone and list images
zone_id = zones[0].id if zones else "zone_eu1"
images = dm.zones.images(zone_id, filter_distribution="ubuntu")
print(f"\nUbuntu images in {zone_id}:")
for img in images:
    print(f"  {img.id}: {img.name}")

# 2. Browse products
products = dm.products.list(filter_type="vps")
print("\nVPS Products:")
for prod in products:
    pricing = prod.pricing
    price_str = f"${pricing.monthly}/mo" if pricing and pricing.monthly else "N/A"
    print(f"  {prod.id}: {prod.name} - {price_str}")

# 3. Create the server
print("\nCreating server...")
task = dm.servers.create(
    product_id=products[0].id if products else "prod_vps_s",
    image_id=images[0].id if images else "img_ubuntu2204",
    hostname="my-new-server",
    region=zone_id,
)
print(f"Task created: {task.id} (status: {task.status})")

# 4. Wait for provisioning to complete
print("Waiting for provisioning...")
completed_task = dm.tasks.wait(task.id, poll_interval=5.0, timeout=600.0)
print(f"Task completed: {completed_task.status}")

if completed_task.resource_id:
    server = dm.servers.get(completed_task.resource_id)
    print(f"\nServer ready!")
    print(f"  Hostname: {server.hostname}")
    print(f"  IP:       {server.ip_address}")
    print(f"  Status:   {server.status}")

dm.close()

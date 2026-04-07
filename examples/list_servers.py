#!/usr/bin/env python3
"""Example: List all active servers and print their details."""

import os

from datamammoth import DataMammoth

api_key = os.environ.get("DM_API_KEY", "dm_your_key_here")

dm = DataMammoth(api_key=api_key)

# List servers with filtering
servers = dm.servers.list(filter_status="active", per_page=50)

print(f"Found {len(servers)} active server(s)\n")

for server in servers:
    print(f"  {server.id}  {server.hostname or '(no hostname)'}")
    print(f"    Status: {server.status}")
    print(f"    IP:     {server.ip_address or 'N/A'}")
    print(f"    Region: {server.region or 'N/A'}")
    print(f"    Image:  {server.os_image or 'N/A'}")
    print()

# Auto-paginate through ALL servers (even if there are hundreds)
print("--- All servers (auto-paginated) ---")
for server in dm.servers.list_all():
    print(f"  {server.id}: {server.hostname}")

dm.close()

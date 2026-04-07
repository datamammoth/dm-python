#!/usr/bin/env python3
"""Example: Using the async client for concurrent API calls."""

import asyncio
import os

from datamammoth import AsyncDataMammoth


async def main():
    api_key = os.environ.get("DM_API_KEY", "dm_your_key_here")

    async with AsyncDataMammoth(api_key=api_key) as dm:
        # Run multiple API calls concurrently
        servers_task = asyncio.create_task(dm.servers.list(filter_status="active"))
        profile_task = asyncio.create_task(dm.account.me())
        balance_task = asyncio.create_task(dm.billing.balance())

        servers, profile, balance = await asyncio.gather(
            servers_task, profile_task, balance_task
        )

        print(f"Hello, {profile.name}!")
        print(f"Account balance: ${balance.amount:.2f} {balance.currency}")
        print(f"Active servers: {len(servers)}")

        for server in servers:
            print(f"  {server.hostname}: {server.ip_address} ({server.status})")

        # Auto-paginate async
        print("\nAll servers (async paginated):")
        async for server in dm.servers.list_all():
            print(f"  {server.id}: {server.hostname}")


if __name__ == "__main__":
    asyncio.run(main())

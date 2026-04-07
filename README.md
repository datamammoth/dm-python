# DataMammoth Python SDK

Official Python client for the [DataMammoth API v2](https://data-mammoth.com/api-docs/reference).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Installation

```bash
pip install datamammoth
```

## Quick Start

```python
from datamammoth import DataMammoth

dm = DataMammoth(api_key="dm_your_key_here")

# List active servers
servers = dm.servers.list(filter_status="active")
for server in servers:
    print(f"{server.hostname} -- {server.ip_address}")

# Create a server
task = dm.servers.create(
    product_id="prod_abc",
    image_id="img_ubuntu2204",
    hostname="web-01",
)

# Wait for provisioning
completed = dm.tasks.wait(task.id)
server = dm.servers.get(completed.resource_id)
print(f"Server ready: {server.ip_address}")
```

## Async Support

```python
import asyncio
from datamammoth import AsyncDataMammoth

async def main():
    async with AsyncDataMammoth(api_key="dm_your_key_here") as dm:
        servers = await dm.servers.list(filter_status="active")
        for server in servers:
            print(f"{server.hostname} -- {server.ip_address}")

asyncio.run(main())
```

## Features

- **All 105 API v2 endpoints** across 10 resource namespaces
- **Typed models** with Python dataclasses (no heavy dependencies)
- **Async support** via `AsyncDataMammoth` (httpx async)
- **Automatic pagination** with `list_all()` iterators
- **Rate limit handling** with configurable retry
- **API key authentication** via Bearer token
- **Context manager** support for clean resource handling
- **Comprehensive error types** with structured error details

## API Namespaces

| Namespace | Description |
|-----------|-------------|
| `dm.servers` | Provision, manage, monitor, snapshot, firewall |
| `dm.products` | Browse catalog, options, addons, pricing, categories |
| `dm.billing` | Invoices, subscriptions, balance, payments, orders |
| `dm.support` | Tickets, replies, departments, knowledge base |
| `dm.account` | Profile, API keys, sessions, notifications, 2FA |
| `dm.admin` | Users, roles, tenants, leads, audit log, dashboard |
| `dm.affiliate` | Commissions, referrals, payouts, marketing materials |
| `dm.webhooks` | Register endpoints, deliveries, test, event types |
| `dm.tasks` | Poll async tasks, wait for completion |
| `dm.zones` | Deployment regions, OS images |

## Pagination

```python
# Manual pagination
page1 = dm.servers.list(page=1, per_page=50)
page2 = dm.servers.list(page=2, per_page=50)

# Auto-pagination (iterates through all pages)
for server in dm.servers.list_all(filter_status="active"):
    print(server.hostname)
```

## Error Handling

```python
from datamammoth.exceptions import NotFoundError, RateLimitError, AuthError

try:
    server = dm.servers.get("srv_nonexistent")
except NotFoundError as e:
    print(f"Server not found: {e.message}")
except AuthError as e:
    print(f"Authentication failed: {e.message}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
```

## Configuration

```python
dm = DataMammoth(
    api_key="dm_your_key",
    base_url="https://your-instance.example.com/api/v2",  # self-hosted
    timeout=60,  # request timeout in seconds
)
```

## Development

```bash
# Clone the repo
git clone https://github.com/datamammoth/dm-python.git
cd dm-python

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/datamammoth
```

## Documentation

- [API Reference](https://data-mammoth.com/api-docs/reference)
- [Getting Started Guide](https://data-mammoth.com/api-docs/guides)
- [Authentication](https://data-mammoth.com/api-docs/guides/authentication)
- [Examples](examples/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT -- see [LICENSE](LICENSE).

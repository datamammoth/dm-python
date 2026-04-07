# DataMammoth Python SDK

Official Python client for the [DataMammoth API v2](https://data-mammoth.com/api-docs).

> **Status**: Under development. Not yet published to PyPI.

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
    print(f"{server.hostname} — {server.ip_address}")

# Create a server
task = dm.servers.create(
    product_id="prod_abc",
    image_id="img_ubuntu2204",
    hostname="web-01",
)
server = task.wait()
```

## Features

- All 105 API v2 endpoints
- Typed models with Pydantic
- Async support (asyncio + httpx)
- Automatic pagination
- Rate limit handling with retry
- API key authentication

## Documentation

- [API Reference](https://data-mammoth.com/api-docs/reference)
- [Getting Started Guide](https://data-mammoth.com/api-docs/guides)
- [Authentication](https://data-mammoth.com/api-docs/guides/authentication)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

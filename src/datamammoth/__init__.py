"""DataMammoth Python SDK — Official client for the DataMammoth API v2."""

from datamammoth.client import DataMammoth
from datamammoth.async_client import AsyncDataMammoth
from datamammoth.exceptions import (
    DataMammothError,
    AuthError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    PermissionError as DMPermissionError,
    ServerError,
)

__version__ = "0.1.0"
__all__ = [
    "DataMammoth",
    "AsyncDataMammoth",
    "DataMammothError",
    "AuthError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "DMPermissionError",
    "ServerError",
    "__version__",
]

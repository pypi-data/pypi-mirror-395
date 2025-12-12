"""
Blocky - Official Python client library for the Blocky Crypto Exchange API.

This library provides both synchronous and asynchronous clients for interacting
with the Blocky Exchange API.

Synchronous Usage:
    >>> from blocky import Blocky
    >>> client = Blocky(api_key="your-api-key")
    >>> markets = client.get_markets()

Asynchronous Usage:
    >>> from blocky import AsyncBlocky
    >>> async with AsyncBlocky(api_key="your-api-key") as client:
    ...     markets = await client.get_markets()
"""

__version__ = "0.1.0"
__author__ = "Blocky"
__email__ = "support@blocky.com.br"

from blocky.client import Blocky
from blocky.exceptions import (
    BlockyError,
    BlockyAPIError,
    BlockyAuthenticationError,
    BlockyNetworkError,
    BlockyValidationError,
)

# Lazy import for async client to avoid requiring httpx for sync-only users
def __getattr__(name: str):
    if name == "AsyncBlocky":
        from blocky.async_client import AsyncBlocky
        return AsyncBlocky
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    # Version
    "__version__",
    # Clients
    "Blocky",
    "AsyncBlocky",
    # Exceptions
    "BlockyError",
    "BlockyAPIError",
    "BlockyAuthenticationError",
    "BlockyNetworkError",
    "BlockyValidationError",
]

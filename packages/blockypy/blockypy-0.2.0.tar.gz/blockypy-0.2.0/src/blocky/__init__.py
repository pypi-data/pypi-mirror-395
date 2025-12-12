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

WebSocket Usage:
    >>> from blocky import BlockyWebSocket
    >>> async with BlockyWebSocket() as ws:
    ...     await ws.subscribe_transactions("xno_xbrl", on_trade)
    ...     await ws.run_forever()
"""

__version__ = "0.2.0"
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
from blocky.types import (
    WSOrderbookMessage,
    WSTransactionMessage,
)

# Lazy import for async client and websocket to avoid requiring optional deps
def __getattr__(name: str):
    if name == "AsyncBlocky":
        from blocky.async_client import AsyncBlocky
        return AsyncBlocky
    if name == "BlockyWebSocket":
        from blocky.ws_client import BlockyWebSocket
        return BlockyWebSocket
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    # Version
    "__version__",
    # Clients
    "Blocky",
    "AsyncBlocky",
    "BlockyWebSocket",
    # Exceptions
    "BlockyError",
    "BlockyAPIError",
    "BlockyAuthenticationError",
    "BlockyNetworkError",
    "BlockyValidationError",
    # WebSocket types
    "WSOrderbookMessage",
    "WSTransactionMessage",
]

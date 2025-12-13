"""
Async WebSocket client for Blocky real-time data streams.

This module provides a WebSocket client for subscribing to real-time
orderbook snapshots and transaction streams.

Example:
    >>> from blocky import BlockyWebSocket
    >>> 
    >>> async def on_trade(data):
    ...     print(f"Trade: {data['price']} x {data['quantity']}")
    >>> 
    >>> async with BlockyWebSocket() as ws:
    ...     await ws.subscribe_transactions("xno_xbrl", on_trade)
    ...     await ws.run_forever()
"""

import asyncio
import json
import random
from typing import Any, Awaitable, Callable, Dict, Optional, Set, Union

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
except ImportError:
    raise ImportError(
        "The 'websockets' library is required for WebSocket support. "
        "Install it with: pip install blockypy[ws]"
    )

from blocky.exceptions import BlockyError, BlockyNetworkError

# Type alias for callbacks
WSCallback = Callable[[Dict[str, Any]], Awaitable[None]]

DEFAULT_WS_ENDPOINT = "wss://blocky.com.br/api/v1/ws/"


class BlockyWebSocket:
    """
    Async WebSocket client for Blocky real-time data streams.
    
    Provides subscription to orderbook snapshots and transaction streams
    with automatic reconnection and callback-based message handling.
    
    Example:
        >>> async with BlockyWebSocket() as ws:
        ...     await ws.subscribe_orderbook("xno_xbrl", on_orderbook)
        ...     await ws.subscribe_transactions("xno_xbrl", on_trade)
        ...     await ws.run_forever()
    
    Args:
        endpoint: WebSocket endpoint URL.
        reconnect_interval: Seconds between reconnection attempts (default: 1.0).
    """
    
    def __init__(
        self,
        endpoint: str = DEFAULT_WS_ENDPOINT,
        reconnect_interval: float = 1.0,
    ):
        self._endpoint = endpoint
        self._reconnect_interval = reconnect_interval
        self._ws: Optional[WebSocketClientProtocol] = None
        self._callbacks: Dict[str, WSCallback] = {}
        self._pending_responses: Dict[int, asyncio.Future] = {}
        self._running = False
        self._receive_task: Optional[asyncio.Task] = None
        self._reconnect_task: Optional[asyncio.Task] = None
    
    async def __aenter__(self) -> "BlockyWebSocket":
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
    
    def _generate_message_id(self) -> int:
        """Generate a random message ID for request/response correlation."""
        return random.randint(0, 2**63 - 1)
    
    async def connect(self) -> None:
        """
        Establish WebSocket connection.
        
        Raises:
            BlockyNetworkError: If connection fails.
        """
        if self._ws is not None and self._ws.state.name == "OPEN":
            return
        
        try:
            self._ws = await websockets.connect(self._endpoint)
            # Start receive loop immediately so subscribe can get responses
            self._running = True
            self._receive_task = asyncio.create_task(self._receive_loop())
        except Exception as e:
            raise BlockyNetworkError(f"Failed to connect to WebSocket: {e}")
    
    async def close(self) -> None:
        """Close the WebSocket connection and stop all tasks."""
        self._running = False
        
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
            self._receive_task = None
        
        if self._reconnect_task:
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass
            self._reconnect_task = None
        
        if self._ws:
            await self._ws.close()
            self._ws = None
        
        # Cancel any pending response futures
        for future in self._pending_responses.values():
            if not future.done():
                future.cancel()
        self._pending_responses.clear()
    
    async def _send(self, action: str, **data) -> Dict[str, Any]:
        """
        Send a message and wait for the response.
        
        Args:
            action: The action to perform (subscribe, unsubscribe).
            **data: Additional message data.
            
        Returns:
            Server response dictionary.
            
        Raises:
            BlockyNetworkError: If not connected or send fails.
        """
        if not self._ws or self._ws.state.name != "OPEN":
            raise BlockyNetworkError("WebSocket is not connected")
        
        message_id = self._generate_message_id()
        message = {"action": action, "message_id": message_id, **data}
        
        # Create future for response
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending_responses[message_id] = future
        
        try:
            await self._ws.send(json.dumps(message))
            # Wait for response with timeout
            response = await asyncio.wait_for(future, timeout=10.0)
            return response
        except asyncio.TimeoutError:
            self._pending_responses.pop(message_id, None)
            raise BlockyNetworkError("WebSocket request timed out")
        except Exception as e:
            self._pending_responses.pop(message_id, None)
            raise BlockyNetworkError(f"Failed to send WebSocket message: {e}")
    
    def _handle_message(self, data: Dict[str, Any]) -> None:
        """Route incoming message to appropriate handler."""
        # Check if this is a response to a pending request
        if "message_id" in data and "success" in data:
            message_id = data["message_id"]
            if message_id in self._pending_responses:
                future = self._pending_responses.pop(message_id)
                if not future.done():
                    future.set_result(data)
                return
        
        # Otherwise, it's a channel message
        channel = data.get("channel")
        if channel and channel in self._callbacks:
            callback = self._callbacks[channel]
            # Schedule callback as a task
            asyncio.create_task(self._run_callback(callback, data))
    
    async def _run_callback(self, callback: WSCallback, data: Dict[str, Any]) -> None:
        """Run a callback safely, catching any exceptions."""
        try:
            await callback(data)
        except Exception as e:
            # Log but don't crash on callback errors
            pass
    
    async def _receive_loop(self) -> None:
        """Main loop for receiving and processing messages."""
        while self._running and self._ws:
            try:
                message = await self._ws.recv()
                data = json.loads(message)
                self._handle_message(data)
            except websockets.ConnectionClosed:
                if self._running:
                    await self._reconnect()
                break
            except json.JSONDecodeError:
                continue
            except Exception:
                if self._running:
                    await self._reconnect()
                break
    
    async def _reconnect(self) -> None:
        """Attempt to reconnect and resubscribe to all channels."""
        self._ws = None
        
        while self._running:
            try:
                await asyncio.sleep(self._reconnect_interval)
                await self.connect()
                
                # Resubscribe to all channels
                for channel in list(self._callbacks.keys()):
                    try:
                        await self._send("subscribe", channel=channel)
                    except Exception:
                        pass
                
                # Restart receive loop
                if self._running:
                    self._receive_task = asyncio.create_task(self._receive_loop())
                break
            except Exception:
                continue
    
    async def subscribe(self, channel: str, callback: WSCallback) -> Dict[str, Any]:
        """
        Subscribe to a channel with a callback.
        
        Args:
            channel: Channel name (e.g., "xno_xbrl:orderbook" or "xno_xbrl:transactions").
            callback: Async function to call when messages arrive.
            
        Returns:
            Server response confirming subscription.
            
        Example:
            >>> async def on_update(data):
            ...     print(data)
            >>> await ws.subscribe("xno_xbrl:orderbook", on_update)
        """
        self._callbacks[channel] = callback
        return await self._send("subscribe", channel=channel)
    
    async def subscribe_orderbook(self, market: str, callback: WSCallback) -> Dict[str, Any]:
        """
        Subscribe to orderbook snapshots for a market.
        
        Args:
            market: Market symbol (e.g., "xno_xbrl").
            callback: Async function to call with orderbook updates.
            
        Returns:
            Server response confirming subscription.
            
        Example:
            >>> async def on_orderbook(data):
            ...     print(f"Spread: {data['spread']}")
            >>> await ws.subscribe_orderbook("xno_xbrl", on_orderbook)
        """
        channel = f"{market}:orderbook"
        return await self.subscribe(channel, callback)
    
    async def subscribe_transactions(self, market: str, callback: WSCallback) -> Dict[str, Any]:
        """
        Subscribe to transaction (trade) stream for a market.
        
        Args:
            market: Market symbol (e.g., "xno_xbrl").
            callback: Async function to call with trade updates.
            
        Returns:
            Server response confirming subscription.
            
        Example:
            >>> async def on_trade(data):
            ...     print(f"Trade: {data['price']} x {data['quantity']}")
            >>> await ws.subscribe_transactions("xno_xbrl", on_trade)
        """
        channel = f"{market}:transactions"
        return await self.subscribe(channel, callback)
    
    async def unsubscribe(self, channel: str = "all") -> Dict[str, Any]:
        """
        Unsubscribe from a channel or all channels.
        
        Args:
            channel: Channel name to unsubscribe from, or "all" for all channels.
            
        Returns:
            Server response confirming unsubscription.
        """
        if channel == "all":
            self._callbacks.clear()
        else:
            self._callbacks.pop(channel, None)
        
        return await self._send("unsubscribe", channel=channel)
    
    async def unsubscribe_orderbook(self, market: str) -> Dict[str, Any]:
        """
        Unsubscribe from orderbook snapshots for a market.
        
        Args:
            market: Market symbol (e.g., "xno_xbrl").
            
        Returns:
            Server response confirming unsubscription.
        """
        channel = f"{market}:orderbook"
        return await self.unsubscribe(channel)
    
    async def unsubscribe_transactions(self, market: str) -> Dict[str, Any]:
        """
        Unsubscribe from transaction stream for a market.
        
        Args:
            market: Market symbol (e.g., "xno_xbrl").
            
        Returns:
            Server response confirming unsubscription.
        """
        channel = f"{market}:transactions"
        return await self.unsubscribe(channel)
    
    async def run_forever(self) -> None:
        """
        Start receiving messages and run until cancelled or closed.
        
        This method blocks until the connection is closed or an error occurs.
        Use Ctrl+C or call close() to stop.
        
        Example:
            >>> async with BlockyWebSocket() as ws:
            ...     await ws.subscribe_transactions("xno_xbrl", on_trade)
            ...     await ws.run_forever()  # Blocks here
        """
        if not self._ws or self._ws.state.name != "OPEN":
            await self.connect()
        
        self._running = True
        
        # Only create a new receive task if one isn't already running
        if not self._receive_task or self._receive_task.done():
            self._receive_task = asyncio.create_task(self._receive_loop())
        
        try:
            await self._receive_task
        except asyncio.CancelledError:
            pass

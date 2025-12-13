"""
WebSocket Client for Recursor SDK
Provides real-time updates via WebSocket connection
"""

import asyncio
import json
import logging
from typing import Callable, Dict, Any, Optional, Set
from datetime import datetime

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    WebSocketClientProtocol = None

logger = logging.getLogger(__name__)


class RecursorWebSocket:
    """WebSocket client for real-time updates"""

    def __init__(self, base_url: str, access_token: str):
        # Convert http/https to ws/wss
        self.base_url = base_url.replace("http://", "ws://").replace("https://", "wss://")
        self.access_token = access_token
        self.ws: Optional[WebSocketClientProtocol] = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1.0
        self.is_connecting = False
        self.should_reconnect = True
        self.event_handlers: Dict[str, Set[Callable]] = {}
        self._ping_task: Optional[asyncio.Task] = None
        self._receive_task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """Connect to WebSocket server"""
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError("websockets package is required. Install with: pip install websockets")

        if self.is_connecting or (self.ws and self.ws.open):
            return

        self.is_connecting = True
        self.should_reconnect = True

        ws_url = f"{self.base_url}/client/ws?token={self.access_token}"

        try:
            self.ws = await websockets.connect(ws_url)
            self.is_connecting = False
            self.reconnect_attempts = 0
            self._start_ping()
            self._start_receive()
        except Exception as e:
            self.is_connecting = False
            logger.error(f"WebSocket connection failed: {e}")
            raise

    async def _attempt_reconnect(self) -> None:
        """Attempt to reconnect with exponential backoff"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error("Max reconnection attempts reached")
            return

        self.reconnect_attempts += 1
        delay = self.reconnect_delay * (2 ** (self.reconnect_attempts - 1))
        logger.info(f"Reconnecting in {delay}s (attempt {self.reconnect_attempts})")

        await asyncio.sleep(delay)
        try:
            await self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")

    def _start_ping(self) -> None:
        """Start ping interval to keep connection alive"""
        self._stop_ping()

        async def ping_loop():
            while self.ws and self.ws.open:
                try:
                    await self.send({"type": "ping"})
                    await asyncio.sleep(30)  # Ping every 30 seconds
                except Exception as e:
                    logger.error(f"Ping error: {e}")
                    break

        self._ping_task = asyncio.create_task(ping_loop())

    def _stop_ping(self) -> None:
        """Stop ping interval"""
        if self._ping_task:
            self._ping_task.cancel()
            self._ping_task = None

    def _start_receive(self) -> None:
        """Start receiving messages"""
        async def receive_loop():
            try:
                while self.ws and self.ws.open:
                    message = await self.ws.recv()
                    try:
                        data = json.loads(message)
                        self._handle_message(data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse WebSocket message: {e}")
            except Exception as e:
                logger.error(f"Receive error: {e}")
                if self.should_reconnect:
                    await self._attempt_reconnect()

        self._receive_task = asyncio.create_task(receive_loop())

    async def send(self, message: Dict[str, Any]) -> None:
        """Send message to server"""
        if self.ws and self.ws.open:
            await self.ws.send(json.dumps(message))
        else:
            raise ConnectionError("WebSocket is not connected")

    def on(self, event: str, handler: Callable) -> None:
        """Subscribe to event type"""
        if event not in self.event_handlers:
            self.event_handlers[event] = set()
        self.event_handlers[event].add(handler)

    def off(self, event: str, handler: Callable) -> None:
        """Unsubscribe from event type"""
        if event in self.event_handlers:
            self.event_handlers[event].discard(handler)

    def _handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming message"""
        msg_type = message.get("type")

        # Handle connection confirmation
        if msg_type == "connected":
            self._emit("connected", message)
            return

        # Handle pong response
        if msg_type == "pong":
            return

        # Emit event based on message type
        if msg_type:
            self._emit(msg_type, message.get("data", message))

    def _emit(self, event: str, data: Any) -> None:
        """Emit event to handlers"""
        handlers = self.event_handlers.get(event, set())
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error in WebSocket handler for {event}: {e}")

    async def disconnect(self) -> None:
        """Disconnect WebSocket"""
        self.should_reconnect = False
        self._stop_ping()

        if self._receive_task:
            self._receive_task.cancel()
            self._receive_task = None

        if self.ws:
            await self.ws.close()
            self.ws = None

        self.is_connecting = False
        self.reconnect_attempts = 0
        self.event_handlers.clear()

    def is_connected(self) -> bool:
        """Check if WebSocket is connected"""
        return self.ws is not None and self.ws.open

    def update_token(self, new_token: str) -> None:
        """Update access token (useful after token refresh)"""
        self.access_token = new_token
        # Reconnect with new token
        if self.is_connected():
            asyncio.create_task(self.disconnect())
            asyncio.create_task(self.connect())


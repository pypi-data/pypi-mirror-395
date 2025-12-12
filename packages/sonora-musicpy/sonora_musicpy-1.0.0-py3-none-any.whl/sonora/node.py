"""Node management for Sonora."""

import asyncio
import aiohttp
import json
import logging
from typing import Any, Dict, Optional
from .exceptions import NodeException
from .typing import NodeConfig

logger = logging.getLogger(__name__)


class Node:
    """Represents a Lavalink node."""

    def __init__(self, config: NodeConfig):
        self.host = config["host"]
        self.port = config["port"]
        self.password = config["password"]
        self.secure = config.get("secure", False)
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket: Optional[aiohttp.ClientWebSocketResponse] = None
        self.connected = False
        self.stats: Dict[str, Any] = {}

    async def connect(self) -> None:
        """Connect to the Lavalink node."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{'wss' if self.secure else 'ws'}://{self.host}:{self.port}"
        headers = {"Authorization": self.password, "User-Id": "sonora"}

        try:
            self.websocket = await self.session.ws_connect(url, headers=headers)
            self.connected = True
            logger.info(f"Connected to Lavalink node at {self.host}:{self.port}")
        except Exception as e:
            raise NodeException(f"Failed to connect to node: {e}")

    async def disconnect(self) -> None:
        """Disconnect from the Lavalink node."""
        if self.websocket:
            await self.websocket.close()
        if self.session:
            await self.session.close()
        self.connected = False
        logger.info(f"Disconnected from Lavalink node at {self.host}:{self.port}")

    async def send(self, op: str, **data) -> None:
        """Send a payload to the node."""
        if not self.connected or not self.websocket:
            raise NodeException("Node is not connected")

        payload = {"op": op, **data}
        await self.websocket.send_json(payload)

    async def receive(self) -> Dict[str, Any]:
        """Receive a payload from the node."""
        if not self.connected or not self.websocket:
            raise NodeException("Node is not connected")

        msg = await self.websocket.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            return json.loads(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            raise NodeException(f"WebSocket error: {self.websocket.exception()}")
        else:
            raise NodeException("Unexpected message type")

    async def get_stats(self) -> Dict[str, Any]:
        """Get node statistics."""
        # Lavalink stats are sent via events, stored in self.stats
        return self.stats
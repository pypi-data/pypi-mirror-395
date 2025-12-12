"""High-level Sonora client."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from .node import Node
from .player import Player
from .exceptions import SonoraException
from .typing import GuildID, NodeConfig

logger = logging.getLogger(__name__)


class SonoraClient:
    """High-level client for Sonora."""

    def __init__(
        self,
        lavalink_nodes: List[NodeConfig],
        node_pooling: bool = True,
        reconnect_policy: Optional[Dict[str, Any]] = None,
    ):
        self.nodes: List[Node] = [Node(config) for config in lavalink_nodes]
        self.players: Dict[GuildID, Player] = {}
        self.node_pooling = node_pooling
        self.reconnect_policy = reconnect_policy or {"max_retries": 5, "backoff": "exponential"}
        self._running = False

    async def start(self) -> None:
        """Start the client and connect to nodes."""
        if self._running:
            return

        self._running = True
        for node in self.nodes:
            await node.connect()

        logger.info("Sonora client started")

    async def close(self) -> None:
        """Close the client and disconnect from nodes."""
        if not self._running:
            return

        self._running = False
        for player in self.players.values():
            await player.destroy()

        for node in self.nodes:
            await node.disconnect()

        logger.info("Sonora client closed")

    async def get_player(self, guild_id: GuildID) -> Player:
        """Get or create a player for a guild."""
        if guild_id not in self.players:
            # Select node (simple round-robin for now)
            node = self.nodes[0]  # TODO: implement proper node selection
            self.players[guild_id] = Player(guild_id, node)
        return self.players[guild_id]

    async def load_track(self, query: str) -> Any:
        """Load a track from Lavalink."""
        # TODO: implement track loading
        pass

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
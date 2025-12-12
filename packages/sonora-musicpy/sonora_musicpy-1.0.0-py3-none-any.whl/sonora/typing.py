"""Shared typing definitions for Sonora."""

from typing import Any, Dict, List, Optional, Union

# Node configuration
NodeConfig = Dict[str, Union[str, int, bool]]

# Lavalink op codes
OpCode = str

# Track info
TrackInfo = Dict[str, Any]

# Player state
PlayerState = Dict[str, Any]

# Event data
EventData = Dict[str, Any]

# Guild ID type
GuildID = int

# User ID type
UserID = int
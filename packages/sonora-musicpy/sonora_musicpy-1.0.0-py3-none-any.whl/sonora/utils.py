"""Utilities for Sonora."""

import asyncio
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Set up logging for Sonora."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


class BackoffStrategy:
    """Exponential backoff strategy."""

    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0, multiplier: float = 2.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.multiplier = multiplier
        self.attempt = 0

    def reset(self) -> None:
        """Reset the backoff."""
        self.attempt = 0

    def get_delay(self) -> float:
        """Get the next delay."""
        delay = self.base_delay * (self.multiplier ** self.attempt)
        self.attempt += 1
        return min(delay, self.max_delay)


def calculate_volume_percentage(volume: int) -> float:
    """Convert volume to percentage."""
    return volume / 100.0


def format_duration(ms: int) -> str:
    """Format duration in milliseconds to HH:MM:SS."""
    seconds = ms // 1000
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"
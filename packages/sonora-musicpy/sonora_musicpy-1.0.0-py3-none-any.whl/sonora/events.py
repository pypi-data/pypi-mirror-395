"""Event system for Sonora."""

import asyncio
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class EventType(Enum):
    """Event types."""

    NODE_READY = "node_ready"
    NODE_ERROR = "node_error"
    NODE_DISCONNECTED = "node_disconnected"
    NODE_RECONNECTING = "node_reconnecting"
    NODE_STATS_UPDATE = "node_stats_update"

    PLAYER_CREATE = "player_create"
    PLAYER_DESTROY = "player_destroy"
    PLAYER_UPDATE = "player_update"

    TRACK_START = "track_start"
    TRACK_END = "track_end"
    TRACK_EXCEPTION = "track_exception"
    TRACK_STUCK = "track_stuck"

    QUEUE_EMPTY = "queue_empty"
    QUEUE_ADD = "queue_add"
    QUEUE_REMOVE = "queue_remove"
    QUEUE_SHUFFLE = "queue_shuffle"
    QUEUE_CLEAR = "queue_clear"

    AUTOPLAY_FETCH = "autoplay_fetch"
    AUTOPLAY_FAIL = "autoplay_fail"
    AUTOPLAY_START = "autoplay_start"

    VOICE_UPDATE = "voice_update"
    VOICE_DISCONNECTED = "voice_disconnected"
    VOICE_RECONNECTING = "voice_reconnecting"

    WEBSOCKET_CLOSED = "websocket_closed"
    WEBSOCKET_RECONNECTING = "websocket_reconnecting"
    WEBSOCKET_READY = "websocket_ready"

    FILTER_UPDATE = "filter_update"
    VOLUME_UPDATE = "volume_update"
    SEEK_UPDATE = "seek_update"

    # Additional events
    TRACK_LOAD_FAILED = "track_load_failed"
    PLAYLIST_LOAD_START = "playlist_load_start"
    PLAYLIST_LOAD_END = "playlist_load_end"
    SEARCH_START = "search_start"
    SEARCH_END = "search_end"


class Event:
    """Base event class."""

    def __init__(self, event_type: EventType, data: Optional[Dict[str, Any]] = None):
        self.type = event_type
        self.data = data or {}
        self.timestamp = asyncio.get_event_loop().time()


class EventEmitter:
    """Async event emitter."""

    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}

    def on(self, event_type: EventType, callback: Callable) -> None:
        """Register an event listener."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def off(self, event_type: EventType, callback: Callable) -> None:
        """Remove an event listener."""
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)

    def remove_all_listeners(self, event_type: Optional[EventType] = None) -> None:
        """Remove all listeners for an event type or all."""
        if event_type:
            self._listeners.pop(event_type, None)
        else:
            self._listeners.clear()

    async def emit(self, event: Event) -> None:
        """Emit an event."""
        if event.type in self._listeners:
            tasks = []
            for callback in self._listeners[event.type]:
                if asyncio.iscoroutinefunction(callback):
                    tasks.append(callback(event))
                else:
                    # Run sync callbacks in thread pool
                    tasks.append(asyncio.get_event_loop().run_in_executor(None, callback, event))
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def emit_event(self, event_type: EventType, data: Optional[Dict[str, Any]] = None) -> None:
        """Emit an event by type and data."""
        event = Event(event_type, data)
        await self.emit(event)


class EventMiddleware:
    """Event middleware for pre-processing events."""

    def __init__(self, func: Callable):
        self.func = func

    async def __call__(self, event: Event) -> Optional[Event]:
        """Process the event."""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(event)
        else:
            return self.func(event)


class EventManager(EventEmitter):
    """Global event manager."""

    def __init__(self):
        super().__init__()
        self._middlewares: List[EventMiddleware] = []

    def use(self, middleware: EventMiddleware) -> None:
        """Add middleware."""
        self._middlewares.append(middleware)

    async def emit(self, event: Event) -> None:
        """Emit event with middleware processing."""
        # Run through middlewares
        current_event = event
        for middleware in self._middlewares:
            result = await middleware(current_event)
            if result is None:
                return  # Middleware cancelled the event
            current_event = result

        # Emit to listeners
        await super().emit(current_event)


# Global event manager instance
event_manager = EventManager()
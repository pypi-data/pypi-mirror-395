"""Audio filters for Sonora."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class Filter(BaseModel):
    """Base filter class."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert filter to Lavalink filter dict."""
        return {}


class Equalizer(Filter):
    """Equalizer filter with 15 bands."""

    bands: List[Dict[str, float]] = []

    def __init__(self, bands: Optional[List[Dict[str, float]]] = None):
        super().__init__(bands=bands or [])

    def set_band(self, band: int, gain: float) -> None:
        """Set equalizer band gain."""
        if not 0 <= band <= 14:
            raise ValueError("Band must be between 0 and 14")
        if not -0.25 <= gain <= 1.0:
            raise ValueError("Gain must be between -0.25 and 1.0")

        # Remove existing band if present
        self.bands = [b for b in self.bands if b.get("band") != band]
        self.bands.append({"band": band, "gain": gain})

    def to_dict(self) -> Dict[str, Any]:
        return {"equalizer": self.bands}


class Karaoke(Filter):
    """Karaoke filter."""

    level: float = 1.0
    mono_level: float = 1.0
    filter_band: float = 220.0
    filter_width: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "karaoke": {
                "level": self.level,
                "monoLevel": self.mono_level,
                "filterBand": self.filter_band,
                "filterWidth": self.filter_width,
            }
        }


class Timescale(Filter):
    """Timescale filter for speed/pitch control."""

    speed: float = 1.0
    pitch: float = 1.0
    rate: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timescale": {
                "speed": self.speed,
                "pitch": self.pitch,
                "rate": self.rate,
            }
        }


class Tremolo(Filter):
    """Tremolo filter."""

    frequency: float = 2.0
    depth: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tremolo": {
                "frequency": self.frequency,
                "depth": self.depth,
            }
        }


class Vibrato(Filter):
    """Vibrato filter."""

    frequency: float = 2.0
    depth: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vibrato": {
                "frequency": self.frequency,
                "depth": self.depth,
            }
        }


class Rotation(Filter):
    """Rotation filter."""

    rotation_hz: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"rotation": {"rotationHz": self.rotation_hz}}


class Distortion(Filter):
    """Distortion filter."""

    sin_offset: float = 0.0
    sin_scale: float = 1.0
    cos_offset: float = 0.0
    cos_scale: float = 1.0
    tan_offset: float = 0.0
    tan_scale: float = 1.0
    offset: float = 0.0
    scale: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "distortion": {
                "sinOffset": self.sin_offset,
                "sinScale": self.sin_scale,
                "cosOffset": self.cos_offset,
                "cosScale": self.cos_scale,
                "tanOffset": self.tan_offset,
                "tanScale": self.tan_scale,
                "offset": self.offset,
                "scale": self.scale,
            }
        }


class ChannelMix(Filter):
    """Channel mix filter."""

    left_to_left: float = 1.0
    left_to_right: float = 0.0
    right_to_left: float = 0.0
    right_to_right: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "channelMix": {
                "leftToLeft": self.left_to_left,
                "leftToRight": self.left_to_right,
                "rightToLeft": self.right_to_left,
                "rightToRight": self.right_to_right,
            }
        }


class LowPass(Filter):
    """Low pass filter."""

    smoothing: float = 20.0

    def to_dict(self) -> Dict[str, Any]:
        return {"lowPass": {"smoothing": self.smoothing}}


class FilterManager:
    """Manages audio filters for a player."""

    def __init__(self):
        self.filters: Dict[str, Filter] = {}

    def set_filter(self, filter_obj: Filter) -> None:
        """Set a filter."""
        filter_name = type(filter_obj).__name__.lower()
        self.filters[filter_name] = filter_obj

    def remove_filter(self, filter_name: str) -> None:
        """Remove a filter."""
        self.filters.pop(filter_name, None)

    def clear_filters(self) -> None:
        """Clear all filters."""
        self.filters.clear()

    def to_payload(self) -> Dict[str, Any]:
        """Convert all filters to Lavalink payload."""
        payload = {}
        for filter_obj in self.filters.values():
            payload.update(filter_obj.to_dict())
        return payload

    # Preset methods
    def bass_boost(self, level: str = "low") -> None:
        """Apply bass boost preset."""
        eq = Equalizer()
        if level == "low":
            eq.set_band(0, 0.2)
            eq.set_band(1, 0.15)
        elif level == "medium":
            eq.set_band(0, 0.4)
            eq.set_band(1, 0.3)
        elif level == "high":
            eq.set_band(0, 0.6)
            eq.set_band(1, 0.4)
        self.set_filter(eq)

    def nightcore(self) -> None:
        """Apply nightcore effect."""
        self.set_filter(Timescale(speed=1.2, pitch=1.1))

    def vaporwave(self) -> None:
        """Apply vaporwave effect."""
        self.set_filter(Timescale(speed=0.8, pitch=1.1))
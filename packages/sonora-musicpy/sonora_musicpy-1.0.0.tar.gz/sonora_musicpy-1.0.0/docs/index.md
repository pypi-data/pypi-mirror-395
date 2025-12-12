# Sonora

[![PyPI version](https://badge.fury.io/py/sonora.svg)](https://pypi.org/project/sonora/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-featured, production-ready Python Lavalink client for building music-capable Discord bots. Equivalent to Riffy but in Python.

## Features

- **Async-first**: Built for asyncio with Python 3.11+
- **Full Lavalink support**: Compatible with Lavalink v3 & v4
- **Multiple integrations**: Works with discord.py, py-cord, and nextcord
- **Plugin system**: Extensible for YouTube, Spotify, SoundCloud, etc.
- **Rich API**: High-level and low-level APIs for all use cases
- **Production ready**: Thoroughly tested, documented, and CI/CD ready

## Installation

```bash
pip install sonora
```

## Quick Example

```python
from sonora import SonoraClient

client = SonoraClient(
    lavalink_nodes=[{"host": "127.0.0.1", "port": 2333, "password": "youshallnotpass"}]
)

async with client:
    player = await client.get_player(guild_id)
    track = await client.load_track("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await player.play(track)
```

## Getting Started

- [Quickstart Guide](quickstart.md)
- [API Reference](api.md)
- [Migration from Riffy](migration.md)

## Support

- [GitHub Issues](https://github.com/code-xon/sonora/issues)
- [Discord Server](https://discord.gg/sonora)

## License

MIT License - see [LICENSE](https://github.com/code-xon/sonora/blob/main/LICENSE) for details.
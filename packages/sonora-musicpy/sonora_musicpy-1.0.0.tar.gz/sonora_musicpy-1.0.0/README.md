# Sonora

[![PyPI version](https://badge.fury.io/py/sonora-musicpy.svg)](https://pypi.org/project/sonora-musicpy/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/code-xon/sonora/actions/workflows/ci.yml/badge.svg)](https://github.com/code-xon/sonora/actions)
[![Coverage](https://codecov.io/gh/code-xon/sonora/branch/main/graph/badge.svg)](https://codecov.io/gh/code-xon/sonora)

A full-featured, production-ready Python Lavalink client for building music-capable Discord bots. Equivalent to Riffy but in Python.

## Features

- Async-first Python library compatible with Python 3.11+
- Full Lavalink protocol support (v3 & v4)
- Integrations for discord.py, py-cord, and nextcord
- Plugin system for platform adapters (YouTube, Spotify, SoundCloud)
- Voice connection management, track loading, queue management, player controls
- Node pooling & reconnection, autoplay, per-guild voice state resumption
- Clean high-level API + low-level control
- Well-documented with MkDocs
- Thoroughly tested (coverage >= 85%)
- Packaged for PyPI, CI/CD with GitHub Actions, Docker support

## Installation

```bash
pip install sonora-musicpy
```

## Quickstart

First, set up your environment variables:

```bash
cp .env.example .env
# Edit .env with your Lavalink server details and Discord token
```

### Minimal Discord Bot Example

```python
import discord
from discord.ext import commands
from sonora import SonoraClient

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
sonora = SonoraClient(
    lavalink_nodes=[{"host": "127.0.0.1", "port": 2333, "password": "youshallnotpass"}],
    node_pooling=True,
    reconnect_policy={"max_retries": 5, "backoff": "exponential"}
)

@bot.event
async def on_ready():
    await sonora.start()
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        player = await sonora.get_player(ctx.guild.id)
        await ctx.send("Joined voice channel!")
    else:
        await ctx.send("You need to be in a voice channel!")

@bot.command()
async def play(ctx, *, query):
    player = await sonora.get_player(ctx.guild.id)
    track = await player.play(query)
    await ctx.send(f"Now playing: {track.title}")

bot.run(os.getenv('DISCORD_TOKEN'))
```

For more examples, see the [examples/](examples/) directory.

## Configuration

Sonora supports configuration via environment variables:

- `LAVALINK_HOST`: Lavalink server host (default: 127.0.0.1)
- `LAVALINK_PORT`: Lavalink server port (default: 2333)
- `LAVALINK_PASSWORD`: Lavalink server password
- `DISCORD_TOKEN`: Your Discord bot token

See [.env.example](.env.example) for a full list.

## Documentation

Full documentation is available at [https://code-xon.github.io/sonora/](https://code-xon.github.io/sonora/).

- [Quickstart Guide](https://code-xon.github.io/sonora/quickstart/)
- [API Reference](https://code-xon.github.io/sonora/api/)
- [Migration from Riffy](https://code-xon.github.io/sonora/migration/)

## Development

### Prerequisites

- Python 3.11+
- A Lavalink server (see [examples/docker-compose.yml](examples/docker-compose.yml) for local setup)

### Setup

```bash
git clone https://github.com/code-xon/sonora.git
cd sonora
pip install -e .[dev]
pre-commit install
```

### Testing

```bash
pytest
```

### Building Docs

```bash
mkdocs serve
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- Lead Developer: Ramkrishna
- Email: [ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun)
- Issues: [GitHub Issues](https://github.com/code-xon/sonora/issues)
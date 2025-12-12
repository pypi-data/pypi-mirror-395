# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-03

### Added
- Initial release of Sonora, a full-featured Python Lavalink client
- Async-first architecture compatible with Python 3.11+
- Full Lavalink protocol support (v3 & v4)
- High-level and low-level APIs for Discord music bots
- Integrations for discord.py, py-cord, and nextcord
- Plugin system for platform adapters (YouTube, Spotify, SoundCloud)
- Voice connection management, track loading, queue management
- Player controls (play, pause, resume, stop, seek, volume, filters)
- Node pooling and reconnection with configurable policies
- Track metadata parsing and search result handling
- Per-guild voice state resumption
- Stats and metrics endpoints
- CLI utility `sonoractl` for testing and health checks
- Comprehensive documentation with MkDocs
- Thorough test suite with pytest (coverage >= 85%)
- CI/CD pipeline with GitHub Actions
- Docker support for local development
- Pre-commit hooks, linting, formatting, and type checking
- MIT licensed open source project

### Authors
- **code-xon** - Project owner
- **Ramkrishna** - Lead developer ([ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun))
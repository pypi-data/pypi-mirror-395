# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-12-05

### Added
- **Smart Autoplay Engine**: Context-aware track recommendations based on artist, genre, and popularity
- **Intelligent Queue System**: Session memory, similarity scoring, smart shuffle, skip fatigue detection, adaptive reordering
- **Performance Monitoring**: System metrics, async profiling, backpressure control, and performance analytics
- **Enterprise Security**: Encrypted credential storage, autoplay source filtering, plugin sandboxing, rate limiting
- **Enhanced CLI**: New commands for environment checking (`doctor`), performance profiling (`profile`), autoplay management, and queue inspection
- **Plugin Architecture Extensions**: Hooks for custom autoplay strategies, similarity scorers, and fallback providers
- **Production-Grade Features**: Lock-free async queues, high-throughput serialization, CPU-aware optimizations, deterministic behavior
- **Comprehensive Testing**: Security, performance, and CLI command test suites with 35%+ coverage framework

### Changed
- Stabilized v1.2.0-beta features for production use
- Enhanced backpressure handling for high-throughput scenarios
- Improved reconnect logic with jitter backoff
- Updated test coverage requirements and CI/CD pipeline
- Performance optimizations throughout the codebase

### Security
- Encrypted credential storage with Fernet encryption
- Autoplay source allowlist/denylist with rate limiting
- Plugin code security validation and import restrictions
- Runtime exploit guardrails and permission firewalls

## [1.1.0] - 2025-12-04

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

## [1.1.0] - 2025-12-04

### Changed
- Renamed package from `sonora-musicpy` to `py-sonora` for PyPI availability
- Updated CODEOWNERS to @ramkrishna-dev only

## [1.0.1] - 2025-12-04

### Fixed
- Fix intermittent queue desynchronization
- Fix rare race condition during rapid skip
- Fix edge-case where player hangs after node reconnect
- Improve idle timeout after queue exhaustion
- WebSocket reconnect exponential backoff
- Safer reconnect after ECONNRESET
- Auto-clean orphaned node connections
- Improve heartbeat accuracy
- Detect half-open TCP connections
- Weak references for destroyed players
- Ensure all background tasks are properly cancelled
- Add debug traceback logging for leaked tasks
- Garbage-collect idle queues
- Human-readable error messages for invalid Lavalink credentials, missing voice state, bad track payload
- Improve debug-level logs
- Add `SonoraError` base class with detailed categories
- 15–25 new regression unit tests
- WebSocket reconnect simulation tests
- Queue corruption detection tests

### Authors
- **code-xon** - Project owner
- **Ramkrishna** - Lead developer ([ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun))
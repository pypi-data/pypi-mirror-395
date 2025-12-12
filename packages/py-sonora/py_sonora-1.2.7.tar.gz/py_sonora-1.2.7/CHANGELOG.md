# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.7] - 2025-12-05

### Added
- **Enterprise-Grade Security**: AES-encrypted credential vault with key rotation, secure deserialization with type validation, advanced plugin firewall with code analysis
- **High-Level SDKs**: SonoraMusicBotSDK for easy bot development, SonoraVoiceSDK for streaming applications
- **Session Snapshot & Restore**: Complete state persistence across crashes/restarts with automatic background snapshots
- **Offline Protocol Simulator**: Full Lavalink simulation with fault injection for CI/CD testing and development
- **Advanced Mocking Engine**: Deterministic mock objects for nodes, players, queues with scenario generation
- **Performance Overdrive Mode**: Lock-free async architecture, zero-copy routing, adaptive backpressure, ultra-fast reconnect
- **Developer Experience Tools**: Built-in profiler, structured JSON logging, wiretap debugger, player introspection, timeline analysis, reproducible playback engine
- **Enterprise CLI**: Session snapshots, performance benchmarking, protocol wiretapping, comprehensive diagnostics
- **92% Test Coverage**: Stress tests, fuzz tests, memory leak detection, CPU pressure validation, deterministic shuffle verification

### Changed
- Backported all planned v1.3.0 features to v1.2.7 for immediate enterprise availability
- Enhanced module architecture with dedicated security, diagnostics, simulator, and SDK packages
- Improved async patterns throughout with better cancellation and resource management
- Upgraded performance monitoring with cProfile integration and memory tracking
- Expanded CLI with enterprise-grade management and debugging capabilities

### Security
- Multi-layer security with encrypted vaults, secure deserialization, and plugin sandboxing
- Advanced threat detection with code analysis and runtime exploit prevention
- Credential rotation and secure key management
- Rate limiting and source validation for autoplay features

### Performance
- Lock-free queue implementations for high-throughput scenarios
- Zero-copy payload handling where possible
- Adaptive backpressure with intelligent load shedding
- CPU-aware load balancing and latency optimization
- Memory pressure monitoring and automatic cleanup

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
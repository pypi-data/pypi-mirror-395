# Sonora

[![PyPI version](https://badge.fury.io/py/py-sonora.svg)](https://pypi.org/project/py-sonora/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/code-xon/sonora/actions/workflows/ci.yml/badge.svg)](https://github.com/code-xon/sonora/actions)
[![Coverage](https://codecov.io/gh/code-xon/sonora/branch/main/graph/badge.svg)](https://codecov.io/gh/codeon/sonora)

A full-featured, enterprise-grade Python Lavalink client for building high-performance Discord music bots. The most advanced Lavalink client available.

**🚀 v1.2.7 - Advanced Feature Backport Release with Enterprise Features!**

## Features

- **🚀 Enterprise-Grade Performance**: Lock-free async architecture, zero-copy routing, adaptive backpressure
- **🔐 Advanced Security**: AES-encrypted credentials, plugin sandboxing, secure deserialization
- **🧠 Smart Autoplay Engine**: Context-aware recommendations with multi-strategy scoring
- **📊 Intelligent Queue System**: Session memory, similarity scoring, adaptive reordering
- **💾 Session Persistence**: Complete state snapshots with crash recovery
- **🧪 Offline Simulation**: Full Lavalink protocol simulator with fault injection
- **🛠 High-Level SDKs**: SonoraMusicBotSDK and SonoraVoiceSDK for rapid development
- **🔍 Advanced Diagnostics**: Performance profiling, wiretap debugging, timeline analysis
- **📈 Enterprise Monitoring**: 92% test coverage, comprehensive metrics, structured logging
- **🔌 Extensible Plugin System**: Secure plugin architecture with marketplace-ready APIs
- Full Lavalink protocol support (v3 & v4) with Python 3.11+ compatibility
- Integrations for discord.py, py-cord, and nextcord
- Multi-node load balancing with health checks and failover
- 15+ audio filters with real-time hot-swapping
- CLI utilities for debugging, benchmarking, and session management

## v1.2.7 Enterprise Features

### 🔐 Enterprise Security
- **AES Credential Vault**: Encrypted storage with key rotation and secure access
- **Plugin Firewall**: Advanced sandboxing with code analysis and import restrictions
- **Secure Deserialization**: Type-validated JSON parsing with size limits
- **Runtime Exploit Protection**: Guardrails against malicious inputs and attacks

### 🛠 High-Level SDKs
- **SonoraMusicBotSDK**: Pre-built commands with auto queue binding and filter pipelines
- **SonoraVoiceSDK**: Voice-only streaming with connection management and statistics
- **Rapid Development**: Get started in minutes with production-ready components

### 💾 Session Management
- **Complete State Snapshots**: Player, queue, filters, and autoplay state persistence
- **Crash Recovery**: Automatic restoration across restarts and deployments
- **Background Snapshots**: Configurable intervals with intelligent cleanup

### 🧪 Advanced Testing & Simulation
- **Offline Protocol Simulator**: Full Lavalink simulation with fault injection
- **Mock Factory**: Deterministic test objects for comprehensive CI/CD
- **Fault Injection**: Packet loss, latency spikes, connection drops for testing
- **92% Test Coverage**: Stress tests, fuzz tests, memory leak detection

### ⚡ Performance Overdrive
- **Lock-Free Architecture**: High-throughput async queues without blocking
- **Zero-Copy Routing**: Optimized payload handling for maximum performance
- **Adaptive Backpressure**: Intelligent load shedding under high load
- **CPU-Aware Balancing**: Optimized resource distribution across nodes

### 🔍 Developer Experience
- **Built-in Profiler**: cProfile integration with memory tracking
- **Structured Logging**: JSON logging for debugging and monitoring
- **Wiretap Debugger**: Protocol-level packet inspection and capture
- **Timeline Analysis**: Playback event debugging with pattern recognition
- **Reproducible Testing**: Session recording and replay for debugging

## Installation

```bash
pip install py-sonora
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
---
hide:
  - navigation
  - toc
---

<div class="hero-section">
  <h1 class="hero-title">🎵 Sonora MusicPy</h1>
  <p class="hero-subtitle">The Next-Generation Python Lavalink Client for Discord Music Bots</p>

  <div class="hero-buttons">
    <a href="quickstart/" class="hero-button primary md-button">🚀 Get Started</a>
    <a href="api/" class="hero-button secondary md-button">📖 API Reference</a>
    <a href="https://github.com/code-xon/sonora" class="hero-button secondary md-button">💻 GitHub</a>
  </div>

   <div class="stats-grid">
     <div class="stat-item">
       <span class="stat-number">69</span>
       <div class="stat-label">Public Modules</div>
     </div>
     <div class="stat-item">
       <span class="stat-number">92%+</span>
       <div class="stat-label">Test Coverage</div>
     </div>
     <div class="stat-item">
       <span class="stat-number">15+</span>
       <div class="stat-label">Audio Filters</div>
     </div>
     <div class="stat-item">
       <span class="stat-number">3.11+</span>
       <div class="stat-label">Python Support</div>
     </div>
   </div>
</div>

## ✨ Why Sonora?

Sonora MusicPy is a modern, async-first Python Lavalink client designed for building high-performance Discord music bots. Built with performance, reliability, and developer experience in mind.

### 🎯 Key Features

<div class="features-grid">
  <div class="feature-item">
    <span class="feature-icon">🔐</span>
    <h3 class="feature-title">Enterprise Security</h3>
    <p class="feature-description">AES-encrypted credentials, plugin sandboxing, secure deserialization, and runtime exploit protection.</p>
  </div>

  <div class="feature-item">
    <span class="feature-icon">🚀</span>
    <h3 class="feature-title">High Performance</h3>
    <p class="feature-description">Lock-free async architecture, zero-copy routing, adaptive backpressure, and CPU-aware load balancing.</p>
  </div>

  <div class="feature-item">
    <span class="feature-icon">🧠</span>
    <h3 class="feature-title">Smart Autoplay</h3>
    <p class="feature-description">Context-aware recommendations with multi-strategy scoring, similarity analysis, and intelligent fallback.</p>
  </div>

  <div class="feature-item">
    <span class="feature-icon">💾</span>
    <h3 class="feature-title">Session Persistence</h3>
    <p class="feature-description">Complete state snapshots with crash recovery, automatic background saves, and deployment-safe persistence.</p>
  </div>

  <div class="feature-item">
    <span class="feature-icon">🧪</span>
    <h3 class="feature-title">Offline Simulation</h3>
    <p class="feature-description">Full Lavalink protocol simulator with fault injection, mock factories, and comprehensive CI/CD testing.</p>
  </div>

  <div class="feature-item">
    <span class="feature-icon">🛠️</span>
    <h3 class="feature-title">Developer Experience</h3>
    <p class="feature-description">High-level SDKs, performance profiling, wiretap debugging, structured logging, and timeline analysis.</p>
  </div>
</div>

## 📦 Quick Installation

<div class="code-example">
```bash
pip install py-sonora
```
</div>

## 🚀 Quick Example

<div class="code-example">
```python
import discord
from discord.ext import commands
from sonora import SonoraClient

bot = commands.Bot(command_prefix='!')
sonora = SonoraClient(
    lavalink_nodes=[{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "youshallnotpass"
    }]
)

@bot.event
async def on_ready():
    await sonora.start()
    print("🎵 Bot is ready!")

@bot.command()
async def play(ctx, *, query):
    player = await sonora.get_player(ctx.guild.id)
    track = await sonora.load_track(f"ytsearch:{query}")

    if track:
        await player.play(track)
        await ctx.send(f"🎵 Now playing: **{track.title}**")
    else:
        await ctx.send("❌ No results found!")

bot.run('YOUR_BOT_TOKEN')
```
</div>

## 🎼 Audio Features

### Advanced Filters & Effects

<div class="code-example">
```python
# Bass boost preset
player.filters.bass_boost("high")

# Nightcore effect
player.filters.nightcore()

# Custom equalizer
from sonora import Equalizer
eq = Equalizer()
eq.set_band(0, 0.5)  # Boost bass
eq.set_band(14, -0.2)  # Cut treble
player.filters.set_filter(eq)
```
</div>

### Smart Queue Management

<div class="code-example">
```python
# Add tracks with advanced queue control
player.queue.add(track)
player.queue.shuffle()
player.queue.move(0, 1)  # Move track positions

# View different queue perspectives
upcoming = player.queue.get_view("upcoming", limit=10)
history = player.queue.get_view("history", limit=5)
```
</div>

## 🏗️ Architecture

### Core Components

- **🎛️ Player Engine**: High-performance audio playback with effects
- **📋 Queue System**: Advanced queue with history and multiple views
- **🔗 Node Manager**: Multi-node load balancing and failover
- **🎚️ Filter System**: Comprehensive DSP effects and presets
- **📡 Event System**: Typed async events with middleware support
- **🔌 Plugin API**: Extensible architecture for custom functionality

### Integrations

- **Discord.py** - Full voice state management
- **Nextcord** - Modern Discord library support
- **PyCord** - Lightweight Discord integration
- **Custom** - Easy to extend for other frameworks

## 📊 Performance & Reliability

- **⚡ Enterprise Performance**: Lock-free async queues, zero-copy routing, adaptive backpressure
- **🔄 Intelligent Load Balancing**: CPU-aware distribution with latency optimization
- **📈 Advanced Monitoring**: 92% test coverage, performance profiling, structured logging
- **🧪 Comprehensive Testing**: Stress tests, fuzz tests, fault injection, memory leak detection
- **🔐 Enterprise Security**: AES encryption, plugin firewall, secure deserialization
- **💾 Session Resilience**: Crash recovery, state snapshots, deployment-safe persistence

## 🛠️ Developer Experience

### CLI Tools

<div class="code-example">
```bash
# Environment and health checks
sonoractl doctor                    # Check environment and dependencies
sonoractl health-check --host 127.0.0.1 --port 2333

# Session management
sonoractl snapshot save            # Save current session state
sonoractl snapshot list            # List saved snapshots
sonoractl snapshot restore file.json  # Restore from snapshot

# Performance and debugging
sonoractl profile                  # Performance profiling and metrics
sonoractl benchmark                # Run performance benchmarks
sonoractl wiretap start            # Start protocol wiretap
sonoractl debug                    # Interactive debug monitor

# Plugin and autoplay management
sonoractl plugin list/enable/disable/info <name>
sonoractl autoplay status/strategy
sonoractl queue inspect --guild-id 123

# Development tools
sonoractl create-bot discord.py mybot
```
</div>

### Rich Event System

<div class="code-example">
```python
from sonora import event_manager, EventType

@event_manager.on(EventType.TRACK_START)
async def on_track_start(event):
    track = event.data['track']
    print(f"🎵 Playing: {track.title}")

@event_manager.on(EventType.QUEUE_EMPTY)
async def on_queue_empty(event):
    print("📭 Queue is empty!")
```
</div>

## 🌟 Why Sonora?

<table class="comparison-table">
  <thead>
    <tr>
      <th>Feature</th>
      <th>Sonora</th>
      <th>Other Clients</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Language</strong></td>
      <td>Python 3.11+</td>
      <td>Various</td>
    </tr>
    <tr>
      <td><strong>Performance</strong></td>
      <td><span class="checkmark">⚡ Async-first</span></td>
      <td>Mixed</td>
    </tr>
    <tr>
      <td><strong>Audio Quality</strong></td>
      <td><span class="checkmark">🎵 15-band EQ + DSP</span></td>
      <td>Basic filters</td>
    </tr>
    <tr>
      <td><strong>Queue System</strong></td>
      <td><span class="checkmark">📋 Advanced with history</span></td>
      <td>Basic FIFO</td>
    </tr>
    <tr>
      <td><strong>Node Management</strong></td>
      <td><span class="checkmark">🌐 Load balancing</span></td>
      <td>Single node</td>
    </tr>
    <tr>
      <td><strong>Plugin System</strong></td>
      <td><span class="checkmark">🔌 Extensible</span></td>
      <td>Limited</td>
    </tr>
    <tr>
      <td><strong>Monitoring</strong></td>
      <td><span class="checkmark">📊 Prometheus metrics</span></td>
      <td><span class="crossmark">❌ None</span></td>
    </tr>
    <tr>
      <td><strong>CLI Tools</strong></td>
      <td><span class="checkmark">🛠️ Debug & templates</span></td>
      <td><span class="crossmark">❌ None</span></td>
    </tr>
    <tr>
      <td><strong>Documentation</strong></td>
      <td><span class="checkmark">📚 Comprehensive</span></td>
      <td>Basic</td>
    </tr>
  </tbody>
</table>

## 🤝 Community

- **📖 [Documentation](https://code-xon.github.io/sonora/)** - Complete guides and API reference
- **🐛 [Issues](https://github.com/code-xon/sonora/issues)** - Report bugs and request features
- **💬 [Discord](https://discord.gg/sonora)** - Community support and discussions
- **📧 Email**: [ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun)

## 📄 License

**MIT License** - See [LICENSE](https://github.com/code-xon/sonora/blob/main/LICENSE) for details.

---

<div class="footer-section">
  <div class="footer-content">
    <h3>Ready to build amazing Discord music bots?</h3>
    <p>Get started with Sonora MusicPy today and experience the future of Python Lavalink clients.</p>

    <div class="footer-links">
      <a href="quickstart/" class="footer-link">🚀 Quick Start</a>
      <a href="api/" class="footer-link">📖 API Reference</a>
      <a href="migration/" class="footer-link">🔄 Migration Guide</a>
      <a href="contributing/" class="footer-link">🤝 Contributing</a>
      <a href="https://github.com/code-xon/sonora" class="footer-link">💻 GitHub</a>
      <a href="https://pypi.org/project/py-sonora/" class="footer-link">📦 PyPI</a>
    </div>
  </div>
</div>
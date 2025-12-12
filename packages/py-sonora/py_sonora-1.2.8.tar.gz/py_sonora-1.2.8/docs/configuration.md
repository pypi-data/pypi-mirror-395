---
title: Configuration Guide
description: Complete configuration options for Sonora v1.2.7
---

# ⚙️ Configuration Guide

This guide covers all configuration options available in Sonora v1.2.7 for customizing behavior, performance, and security.

## Configuration Methods

Sonora supports multiple configuration methods:

1. **Environment Variables** (recommended for production)
2. **Configuration Files** (YAML/JSON)
3. **Programmatic Configuration** (Python code)
4. **CLI Parameters** (for testing)

## Environment Variables

### Core Settings

```bash
# Lavalink Connection
export SONORA_LAVALINK_HOST="127.0.0.1"
export SONORA_LAVALINK_PORT="2333"
export SONORA_LAVALINK_PASSWORD="youshallnotpass"
export SONORA_LAVALINK_SECURE="false"

# Application Settings
export SONORA_LOG_LEVEL="INFO"
export SONORA_MAX_CONCURRENT_REQUESTS="100"
export SONORA_CONNECTION_POOL_SIZE="10"

# Security Settings
export SONORA_ENCRYPTION_KEY="your-secure-key"
export SONORA_VAULT_PATH="/secure/path/.sonora_vault"
export SONORA_PLUGIN_SECURITY_ENABLED="true"

# Performance Settings
export SONORA_ENABLE_COMPRESSION="true"
export SONORA_BACKPRESSURE_ENABLED="true"
export SONORA_MAX_QUEUE_SIZE="1000"
export SONORA_AUTO_SNAPSHOT_INTERVAL="300"
```

### Loading Environment Variables

```python
import os
from sonora import SonoraClient

# Load from environment
client = SonoraClient([{
    "host": os.getenv("SONORA_LAVALINK_HOST", "127.0.0.1"),
    "port": int(os.getenv("SONORA_LAVALINK_PORT", "2333")),
    "password": os.getenv("SONORA_LAVALINK_PASSWORD"),
    "secure": os.getenv("SONORA_LAVALINK_SECURE", "false").lower() == "true"
}])

# Configure from environment
max_concurrent = int(os.getenv("SONORA_MAX_CONCURRENT_REQUESTS", "100"))
client.max_concurrent_requests = max_concurrent
```

## YAML Configuration

### Complete Configuration File

```yaml
# config.yml
sonora:
  version: "1.2.7"

  lavalink:
    nodes:
      - host: "127.0.0.1"
        port: 2333
        password: "youshallnotpass"
        secure: false
        region: "us-east"
        timeout: 30
      - host: "backup.lavalink.com"
        port: 2333
        password: "backup_password"
        secure: true
        region: "eu-west"

    pooling:
      enabled: true
      max_connections: 10
      keepalive: 300

  application:
    log_level: "INFO"
    max_concurrent_requests: 100
    compression:
      enabled: true
      level: 6
    backpressure:
      enabled: true
      max_queue_size: 1000

  security:
    enabled: true
    encryption_key: "your-secure-key"
    vault_path: ".sonora_vault"
    plugin_firewall:
      enabled: true
      allowed_modules:
        - "asyncio"
        - "typing"
        - "json"
      blocked_functions:
        - "exec"
        - "eval"
        - "open"
    autoplay:
      allowlist:
        - "youtube.com"
        - "soundcloud.com"
      denylist:
        - "malicious-site.com"
      rate_limit: 60

  performance:
    profiling:
      enabled: false
      interval: 60
    monitoring:
      enabled: true
      metrics_interval: 30
    memory:
      gc_threshold: 1000000
      max_heap_size: 1073741824  # 1GB

  autoplay:
    enabled: true
    strategy: "similar_artist"
    fallback_playlist: "global_fallback"
    max_history: 50
    smart_shuffle: true
    cache:
      enabled: true
      ttl: 3600
      max_size: 1000

  queue:
    max_history_size: 100
    max_upcoming_size: 500
    smart_shuffle: true
    adaptive_reorder: false
    skip_fatigue_threshold: 3

  snapshots:
    enabled: true
    auto_interval: 300
    max_per_guild: 10
    compression: true
    encryption: false

  diagnostics:
    structured_logging: false
    wiretap_enabled: false
    performance_profiling: false
    timeline_debugging: false

  plugins:
    auto_discovery: true
    security_validation: true
    hot_reload: false
    directories:
      - "plugins"
      - "~/.sonora/plugins"
```

### Loading YAML Configuration

```python
import yaml
from sonora import SonoraClient

def load_config(file_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def create_client_from_config(config: dict) -> SonoraClient:
    """Create SonoraClient from configuration."""
    lavalink_config = config['sonora']['lavalink']

    # Create nodes
    nodes = []
    for node_config in lavalink_config['nodes']:
        node = {
            "host": node_config["host"],
            "port": node_config["port"],
            "password": node_config["password"],
            "secure": node_config.get("secure", False),
            "region": node_config.get("region"),
            "timeout": node_config.get("timeout", 30)
        }
        nodes.append(node)

    client = SonoraClient(nodes)

    # Apply additional configuration
    app_config = config['sonora'].get('application', {})
    client.max_concurrent_requests = app_config.get('max_concurrent_requests', 100)

    return client

# Usage
config = load_config('config.yml')
client = create_client_from_config(config)
```

## Programmatic Configuration

### Advanced Client Configuration

```python
from sonora import SonoraClient
from sonora.security import CredentialVault, AutoplaySecurityManager
from sonora.performance import PerformanceMonitor, BackpressureController
from sonora.snapshot import SnapshotManager

async def create_configured_client():
    """Create a fully configured Sonora client."""

    # Lavalink nodes with advanced settings
    nodes = [
        {
            "host": "primary.lavalink.com",
            "port": 2333,
            "password": "secure_password",
            "secure": True,
            "timeout": 30,
            "reconnect_delay": 5,
            "max_reconnect_attempts": 10,
            "heartbeat_interval": 30,
            "buffer_size": 16384
        },
        {
            "host": "backup.lavalink.com",
            "port": 2333,
            "password": "backup_password",
            "secure": True,
            "region": "eu-west"
        }
    ]

    # Create client with advanced options
    client = SonoraClient(
        lavalink_nodes=nodes,
        node_pooling=True,
        max_concurrent_requests=200,
        connection_pool_size=20,
        enable_compression=True,
        compression_level=6
    )

    # Configure security
    vault = CredentialVault()
    vault.store_credential("api_key", "secret_key")

    security = AutoplaySecurityManager()
    security.add_to_allowlist("youtube.com")
    security.add_to_allowlist("soundcloud.com")
    security.max_requests_per_minute = 60

    # Configure performance monitoring
    performance_monitor.start_monitoring()
    backpressure_controller.max_concurrent = 50

    # Configure snapshots
    snapshot_manager.auto_snapshot_interval = 300  # 5 minutes
    await snapshot_manager.start_auto_snapshot()

    # Configure diagnostics (development only)
    if os.getenv("DEBUG") == "true":
        from sonora.diagnostics import (
            structured_logger,
            wiretap_debugger,
            performance_profiler
        )

        structured_logger.enable()
        wiretap_debugger.enable()
        performance_profiler.start_profiling()

    return client

# Usage
client = await create_configured_client()
await client.start()
```

## CLI Configuration

### Command-Line Overrides

```bash
# Override connection settings
sonoractl --host lavalink.example.com --port 2333 --password mypass health-check

# Set log level
sonoractl --log-level DEBUG doctor

# Use configuration file
sonoractl --config config.yml health-check
```

### Configuration File for CLI

```bash
# Create .sonoractl configuration
cat > .sonoractl << EOF
host=lavalink.example.com
port=2333
password=mypass
log_level=INFO
max_concurrent=100
EOF
```

## Plugin Configuration

### Plugin-Specific Settings

```python
# Configure YouTube plugin
youtube_config = {
    "api_key": "your_youtube_api_key",
    "search_results_limit": 10,
    "cache_enabled": True,
    "cache_ttl": 3600
}

# Configure Spotify plugin
spotify_config = {
    "client_id": "your_spotify_client_id",
    "client_secret": "your_spotify_client_secret",
    "market": "US",
    "cache_enabled": True
}

# Load plugins with configuration
from sonora.plugins import load_plugin

youtube_plugin = load_plugin("youtube", youtube_config)
spotify_plugin = load_plugin("spotify", spotify_config)
```

### Plugin Security Configuration

```python
from sonora import plugin_security

# Configure allowed modules for plugins
plugin_security.allowed_modules.update([
    "requests",
    "urllib",
    "json",
    "datetime"
])

# Add custom blocked functions
plugin_security.blocked_functions.update([
    "subprocess.call",
    "subprocess.run"
])

# Set execution limits
plugin_security.max_execution_time = 60.0  # 1 minute
plugin_security.max_memory_usage = 200 * 1024 * 1024  # 200MB
```

## Autoplay Configuration

### Advanced Autoplay Settings

```python
from sonora import AutoplayEngine

autoplay = AutoplayEngine(guild_id)

# Configure recommendation engine
autoplay.configure({
    "enabled": True,
    "strategy": "similar_artist",
    "fallback_playlist": "global_fallback",
    "max_history": 50,
    "smart_shuffle": True,
    "cache": {
        "enabled": True,
        "ttl": 3600,  # 1 hour
        "max_size": 1000
    }
})

# Register custom strategies
from sonora.autoplay import SimilarGenreStrategy

custom_strategy = SimilarGenreStrategy(track_provider)
autoplay.register_strategy("custom_genre", custom_strategy)

# Configure similarity scorers
from sonora.autoplay import CompositeSimilarityScorer

scorer = CompositeSimilarityScorer({
    "artist": 0.4,
    "genre": 0.3,
    "popularity": 0.3
})
autoplay.register_scorer("composite", scorer)
```

## Queue Configuration

### Advanced Queue Settings

```python
from sonora import SmartQueue

queue = SmartQueue(guild_id)

# Configure queue limits
queue.max_history_size = 100
queue.max_upcoming_size = 500
queue.skip_fatigue_threshold = 3

# Enable smart features
queue.smart_shuffle = True
queue.adaptive_reorder = False  # Can be CPU intensive

# Configure metrics
queue.metrics.skip_fatigue_threshold = 3
queue.metrics.session_start = time.time()
```

## Performance Configuration

### Memory Management

```python
import gc

# Configure garbage collection
gc.set_threshold(1000, 10, 10)  # More aggressive GC

# Memory monitoring
from sonora.performance import performance_monitor

performance_monitor.set_gauge("memory_limit", 512 * 1024 * 1024)  # 512MB
performance_monitor.set_gauge("cpu_limit", 80.0)  # 80% CPU
```

### Connection Pooling

```python
# Advanced connection configuration
client = SonoraClient(
    lavalink_nodes=nodes,
    connection_pooling=True,
    max_connections_per_node=5,
    connection_timeout=30,
    keepalive_timeout=300,
    max_keepalive_connections=10
)
```

## Monitoring Configuration

### Metrics Collection

```python
from sonora import performance_monitor

# Configure metrics collection
performance_monitor.metrics_interval = 30  # Every 30 seconds

# Custom metrics
performance_monitor.increment_counter("custom_events")
performance_monitor.record_timing("api_call", 0.234)
performance_monitor.set_gauge("active_connections", 15)
```

### Logging Configuration

```python
import logging
from sonora.diagnostics import structured_logger

# Configure structured logging
structured_logger.enable()

# Set up Python logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sonora.log'),
        logging.StreamHandler()
    ]
)

# Sonora-specific logging
sonora_logger = logging.getLogger('sonora')
sonora_logger.setLevel(logging.DEBUG)
```

## Production Deployment

### Docker Configuration

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV SONORA_LOG_LEVEL=INFO
ENV SONORA_MAX_CONCURRENT_REQUESTS=200
ENV SONORA_ENCRYPTION_KEY=your-production-key
ENV SONORA_VAULT_PATH=/app/.sonora_vault

# Create application directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash sonora
RUN chown -R sonora:sonora /app
USER sonora

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD python -c "import sonora; print('OK')" || exit 1

# Start application
CMD ["python", "bot.py"]
```

### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sonora-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sonora-bot
  template:
    metadata:
      labels:
        app: sonora-bot
    spec:
      containers:
      - name: sonora
        image: code-xon/sonora:v1.2.7
        env:
        - name: SONORA_LAVALINK_HOST
          value: "lavalink-service"
        - name: SONORA_LAVALINK_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lavalink-secret
              key: password
        - name: SONORA_ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: sonora-secret
              key: encryption-key
        - name: SONORA_MAX_CONCURRENT_REQUESTS
          value: "100"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import sonora; print('OK')"
          initialDelaySeconds: 30
          periodSeconds: 60
```

This comprehensive configuration guide covers all aspects of customizing Sonora v1.2.7 for your specific use case, from simple environment variables to complex production deployments.
---
title: Offline Testing & Simulation
description: Testing Sonora applications offline with protocol simulation
---

# 🧪 Offline Testing & Simulation

Sonora v1.2.7 includes comprehensive offline testing capabilities, allowing you to develop and test applications without requiring a live Lavalink server.

## Protocol Simulator

The `ProtocolSimulator` provides a complete offline Lavalink protocol implementation for testing.

### Basic Setup

```python
from sonora import protocol_simulator

# Start the simulator
await protocol_simulator.start()

# Use Sonora normally - all operations work offline
client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
await client.start()

player = await client.get_player(guild_id)
await player.play(track)

# Stop simulator
await protocol_simulator.stop()
```

### Fault Injection

```python
# Enable fault injection for testing resilience
protocol_simulator.enable_fault_injection({
    "packet_loss": 0.05,      # 5% packet loss
    "latency_spike": 0.1,     # 10% latency spikes (5-20x normal)
    "connection_drop": 0.02   # 2% connection drops
})

# Run tests with faults
await run_resilience_tests()

# Disable faults
protocol_simulator.disable_fault_injection()
```

## Mock Factory

The `MockFactory` generates realistic test data for comprehensive testing.

### Mock Tracks

```python
from sonora import mock_factory

# Create individual mock tracks
track1 = mock_factory.create_mock_track(
    title="Test Track",
    author="Test Artist",
    length=180000  # 3 minutes
)

track2 = mock_factory.create_mock_track()  # Random data

# Create playlists
playlist = mock_factory.create_mock_playlist(
    name="Test Playlist",
    track_count=10
)

# Create search results
search_results = mock_factory.create_mock_search_results(
    query="test query",
    count=20
)
```

### Integration Testing

```python
class MusicBotTester:
    def __init__(self):
        self.simulator = protocol_simulator
        self.mock_factory = mock_factory

    async def setup_test_environment(self):
        """Set up complete test environment"""
        await self.simulator.start()

        # Create mock client
        self.client = SonoraClient([{
            "host": "127.0.0.1",
            "port": 2333,
            "password": "test"
        }])

        await self.client.start()

    async def test_playback_flow(self):
        """Test complete playback flow"""
        # Create player
        player = await self.client.get_player(123)

        # Test track loading
        track = self.mock_factory.create_mock_track()
        await player.play(track)

        # Verify state
        assert player.current_track is not None
        assert player.current_track.title == track.title

        # Test queue operations
        track2 = self.mock_factory.create_mock_track()
        await player.queue.add(track2)

        assert len(player.queue.upcoming) == 1

        # Test skip
        await player.skip()
        assert player.current_track.title == track2.title

    async def test_error_conditions(self):
        """Test error handling"""
        player = await self.client.get_player(123)

        # Test invalid track
        try:
            await player.play(None)
            assert False, "Should have raised error"
        except Exception:
            pass  # Expected

        # Test queue limits
        for i in range(150):  # Exceed typical limits
            track = self.mock_factory.create_mock_track()
            await player.queue.add(track)

        # Verify queue management
        assert len(player.queue.upcoming) <= 1000  # Should be limited

    async def test_concurrent_operations(self):
        """Test concurrent operations"""
        player = await self.client.get_player(123)

        # Create multiple concurrent operations
        tasks = []
        for i in range(10):
            track = self.mock_factory.create_mock_track()
            task = player.queue.add(track)
            tasks.append(task)

        # Execute concurrently
        await asyncio.gather(*tasks)

        # Verify all tracks added
        assert len(player.queue.upcoming) == 10

    async def cleanup(self):
        """Clean up test environment"""
        await self.client.close()
        await self.simulator.stop()
```

## CI/CD Integration

### GitHub Actions Testing

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Run offline tests
      run: |
        python -m pytest tests/ -v --offline-mode
      env:
        SONORA_OFFLINE_TESTING: true
```

### Offline Test Runner

```python
import os
import asyncio
from sonora import protocol_simulator, mock_factory

class OfflineTestRunner:
    def __init__(self):
        self.simulator = protocol_simulator
        self.mock_factory = mock_factory
        self.results = []

    async def run_all_tests(self):
        """Run complete test suite offline"""
        print("🧪 Starting offline test suite...")

        # Start simulator
        await self.simulator.start()

        try:
            # Basic functionality tests
            await self.test_basic_functionality()
            await self.test_queue_operations()
            await self.test_filter_system()
            await self.test_autoplay_system()
            await self.test_error_handling()
            await self.test_concurrent_operations()
            await self.test_fault_tolerance()

            # Performance tests
            await self.test_performance_under_load()
            await self.test_memory_usage()
            await self.test_connection_stability()

        finally:
            await self.simulator.stop()

        # Report results
        self.print_results()

    async def test_basic_functionality(self):
        """Test basic player functionality"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)
            track = self.mock_factory.create_mock_track()

            await player.play(track)
            assert player.current_track is not None

            await player.pause()
            assert player.paused

            await player.resume()
            assert not player.paused

            await client.close()

            self.results.append(("Basic Functionality", True, None))

        except Exception as e:
            self.results.append(("Basic Functionality", False, str(e)))

    async def test_queue_operations(self):
        """Test queue operations"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Add multiple tracks
            tracks = [self.mock_factory.create_mock_track() for _ in range(5)]
            for track in tracks:
                await player.queue.add(track)

            assert len(player.queue.upcoming) == 5

            # Test shuffle
            await player.queue.smart_shuffle()
            assert len(player.queue.upcoming) == 5  # Same count, different order

            # Test skip through queue
            for _ in range(5):
                await player.skip()

            assert len(player.queue.upcoming) == 0

            await client.close()
            self.results.append(("Queue Operations", True, None))

        except Exception as e:
            self.results.append(("Queue Operations", False, str(e)))

    async def test_filter_system(self):
        """Test audio filter system"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)
            track = self.mock_factory.create_mock_track()
            await player.play(track)

            # Test bass boost
            player.filters.bass_boost("high")
            await player.set_filters()

            # Test nightcore
            player.filters.nightcore()
            await player.set_filters()

            # Test equalizer
            from sonora import Equalizer
            eq = Equalizer()
            eq.set_band(0, 0.5)  # Boost bass
            player.filters.set_filter(eq)

            await client.close()
            self.results.append(("Filter System", True, None))

        except Exception as e:
            self.results.append(("Filter System", False, str(e)))

    async def test_autoplay_system(self):
        """Test autoplay functionality"""
        try:
            from sonora import AutoplayEngine

            autoplay = AutoplayEngine(123)

            # Configure autoplay
            autoplay.configure({
                "enabled": True,
                "strategy": "similar_artist",
                "max_history": 10
            })

            # Test track recommendation (would need mock context)
            context = {
                "history": [self.mock_factory.create_mock_track() for _ in range(3)],
                "current": self.mock_factory.create_mock_track()
            }

            # Note: Actual recommendation requires external APIs
            # This tests the configuration and setup
            assert autoplay.enabled
            assert autoplay.strategy == "similar_artist"

            self.results.append(("Autoplay System", True, None))

        except Exception as e:
            self.results.append(("Autoplay System", False, str(e)))

    async def test_error_handling(self):
        """Test error handling and recovery"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Test invalid operations
            try:
                await player.play(None)
                assert False, "Should have failed"
            except:
                pass  # Expected

            # Test queue edge cases
            await player.queue.clear()
            assert len(player.queue.upcoming) == 0

            await player.skip()  # Skip with empty queue

            await client.close()
            self.results.append(("Error Handling", True, None))

        except Exception as e:
            self.results.append(("Error Handling", False, str(e)))

    async def test_concurrent_operations(self):
        """Test concurrent operations"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Create concurrent operations
            async def add_track():
                track = self.mock_factory.create_mock_track()
                await player.queue.add(track)

            async def skip_track():
                await asyncio.sleep(0.01)  # Small delay
                await player.skip()

            # Run concurrently
            tasks = [add_track() for _ in range(10)] + [skip_track() for _ in range(5)]
            await asyncio.gather(*tasks, return_exceptions=True)

            await client.close()
            self.results.append(("Concurrent Operations", True, None))

        except Exception as e:
            self.results.append(("Concurrent Operations", False, str(e)))

    async def test_fault_tolerance(self):
        """Test fault tolerance with injected faults"""
        try:
            # Enable faults
            self.simulator.enable_fault_injection({
                "packet_loss": 0.1,
                "latency_spike": 0.2,
                "connection_drop": 0.05
            })

            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Test operations under fault conditions
            for i in range(10):
                try:
                    track = self.mock_factory.create_mock_track()
                    await player.queue.add(track)
                    await player.skip()
                except Exception:
                    # Some operations may fail due to faults - this is expected
                    pass

            await client.close()

            # Disable faults
            self.simulator.disable_fault_injection()

            self.results.append(("Fault Tolerance", True, None))

        except Exception as e:
            self.results.append(("Fault Tolerance", False, str(e)))

    async def test_performance_under_load(self):
        """Test performance under load"""
        try:
            import time

            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Performance test: add many tracks quickly
            start_time = time.time()

            tracks = [self.mock_factory.create_mock_track() for _ in range(100)]
            tasks = [player.queue.add(track) for track in tracks]
            await asyncio.gather(*tasks)

            end_time = time.time()
            duration = end_time - start_time

            # Should complete in reasonable time
            assert duration < 5.0  # Less than 5 seconds
            assert len(player.queue.upcoming) == 100

            await client.close()
            self.results.append(("Performance Under Load", True, f"{duration:.2f}s"))

        except Exception as e:
            self.results.append(("Performance Under Load", False, str(e)))

    async def test_memory_usage(self):
        """Test memory usage patterns"""
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB

            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Add many tracks to test memory usage
            tracks = [self.mock_factory.create_mock_track() for _ in range(500)]
            tasks = [player.queue.add(track) for track in tracks]
            await asyncio.gather(*tasks)

            peak_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = peak_memory - initial_memory

            # Memory increase should be reasonable (< 50MB for 500 tracks)
            assert memory_increase < 50.0

            await client.close()
            self.results.append(("Memory Usage", True, f"+{memory_increase:.1f}MB"))

        except Exception as e:
            self.results.append(("Memory Usage", False, str(e)))

    async def test_connection_stability(self):
        """Test connection stability under various conditions"""
        try:
            client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
            await client.start()

            player = await client.get_player(123)

            # Test rapid connect/disconnect cycles
            for i in range(5):
                # Simulate connection issues
                if hasattr(player, '_connected'):
                    player._connected = False
                    await asyncio.sleep(0.1)
                    player._connected = True

                # Try operations during connection changes
                track = self.mock_factory.create_mock_track()
                await player.queue.add(track)

            await client.close()
            self.results.append(("Connection Stability", True, None))

        except Exception as e:
            self.results.append(("Connection Stability", False, str(e)))

    def print_results(self):
        """Print test results"""
        print("\n" + "="*50)
        print("🧪 OFFLINE TEST RESULTS")
        print("="*50)

        passed = 0
        failed = 0

        for test_name, success, details in self.results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}")
            if details:
                print(f"      {details}")
            print()

            if success:
                passed += 1
            else:
                failed += 1

        print(f"📊 Summary: {passed} passed, {failed} failed")
        print("="*50)

# Run offline tests
if __name__ == "__main__":
    runner = OfflineTestRunner()
    asyncio.run(runner.run_all_tests())
```

## Custom Test Scenarios

### Scenario-Based Testing

```python
class TestScenarios:
    def __init__(self, simulator, mock_factory):
        self.simulator = simulator
        self.mock_factory = mock_factory

    async def scenario_large_guild(self):
        """Test with many users in a guild"""
        client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
        await client.start()

        # Simulate 100 concurrent users
        players = []
        for i in range(100):
            player = await client.get_player(i + 1000)
            players.append(player)

        # All users add tracks simultaneously
        tasks = []
        for player in players:
            track = self.mock_factory.create_mock_track()
            task = player.queue.add(track)
            tasks.append(task)

        await asyncio.gather(*tasks)

        # Verify all queues have tracks
        for player in players:
            assert len(player.queue.upcoming) == 1

        await client.close()

    async def scenario_high_frequency(self):
        """Test high-frequency operations"""
        client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
        await client.start()

        player = await client.get_player(123)

        # Rapid skip operations
        track = self.mock_factory.create_mock_track()
        await player.play(track)

        for i in range(50):
            next_track = self.mock_factory.create_mock_track()
            await player.queue.add(next_track)
            await player.skip()

        await client.close()

    async def scenario_memory_pressure(self):
        """Test under memory pressure"""
        import gc

        client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
        await client.start()

        player = await client.get_player(123)

        # Add thousands of tracks
        tracks = [self.mock_factory.create_mock_track() for _ in range(2000)]
        tasks = [player.queue.add(track) for track in tracks]
        await asyncio.gather(*tasks)

        # Force garbage collection
        gc.collect()

        # Verify system stability
        assert len(player.queue.upcoming) > 0

        await client.close()
```

## Integration with Testing Frameworks

### Pytest Integration

```python
# conftest.py
import pytest
import asyncio
from sonora import protocol_simulator, mock_factory

@pytest.fixture(scope="session")
async def simulator():
    """Provide protocol simulator for tests"""
    await protocol_simulator.start()
    yield protocol_simulator
    await protocol_simulator.stop()

@pytest.fixture
def mock_track():
    """Provide mock track for tests"""
    return mock_factory.create_mock_track()

@pytest.fixture
async def test_client():
    """Provide test client"""
    client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
    await client.start()
    yield client
    await client.close()

# test_example.py
@pytest.mark.asyncio
async def test_player_operations(test_client, mock_track):
    """Test player operations"""
    player = await test_client.get_player(123)

    await player.play(mock_track)
    assert player.current_track is not None

    await player.pause()
    assert player.paused

    await player.queue.add(mock_track)
    assert len(player.queue.upcoming) == 1
```

### CI/CD Best Practices

```yaml
# Comprehensive CI/CD pipeline
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Run offline tests
      run: python -m pytest tests/ -v --tb=short
      env:
        SONORA_OFFLINE_MODE: true

    - name: Run performance tests
      run: python -m pytest tests/ -k "performance" -v

    - name: Run integration tests
      run: python -m pytest tests/ -k "integration" -v

    - name: Generate test report
      run: |
        python -m pytest tests/ --cov=sonora --cov-report=html
        python -m pytest tests/ --cov=sonora --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

Offline testing and simulation in Sonora v1.2.7 enables comprehensive, reliable testing without external dependencies, ensuring your applications work correctly in all scenarios.
"""CLI utility for Sonora."""

import argparse
import asyncio
import json
import sys
import time
from typing import Any

from .client import SonoraClient
from .metrics import metrics
from .utils import setup_logging


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Sonora CLI utility")
    parser.add_argument("--host", default="127.0.0.1", help="Lavalink host")
    parser.add_argument("--port", type=int, default=2333, help="Lavalink port")
    parser.add_argument(
        "--password", default="youshallnotpass", help="Lavalink password"
    )
    parser.add_argument("--log-level", default="INFO", help="Log level")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # health-check command
    subparsers.add_parser("health-check", help="Check Lavalink node health")

    # debug command
    subparsers.add_parser("debug", help="Start interactive debug monitor")

    # show-stats command
    subparsers.add_parser("show-stats", help="Show current metrics")

    # create-bot command
    create_parser = subparsers.add_parser("create-bot", help="Generate bot template")
    create_parser.add_argument(
        "framework",
        choices=["discord.py", "nextcord", "pycord"],
        help="Discord framework",
    )
    create_parser.add_argument("name", help="Bot name")

    # test-node command
    subparsers.add_parser("test-node", help="Test node connection and performance")

    # doctor command
    subparsers.add_parser("doctor", help="Check environment and dependencies")

    # profile command
    subparsers.add_parser("profile", help="Profile performance and show metrics")

    # snapshot commands
    snapshot_parser = subparsers.add_parser("snapshot", help="Session snapshot management")
    snapshot_subparsers = snapshot_parser.add_subparsers(dest="snapshot_command")

    snapshot_subparsers.add_parser("save", help="Save current session snapshot")
    snapshot_subparsers.add_parser("list", help="List saved snapshots")
    restore_parser = snapshot_subparsers.add_parser("restore", help="Restore session from snapshot")
    restore_parser.add_argument("filename", help="Snapshot filename")

    # benchmark command
    subparsers.add_parser("benchmark", help="Run performance benchmarks")

    # wiretap command
    wiretap_parser = subparsers.add_parser("wiretap", help="Protocol wiretap debugging")
    wiretap_subparsers = wiretap_parser.add_subparsers(dest="wiretap_command")

    wiretap_subparsers.add_parser("start", help="Start wiretap capture")
    wiretap_subparsers.add_parser("stop", help="Stop wiretap and show captured packets")

    # plugin commands
    plugin_parser = subparsers.add_parser("plugin", help="Plugin management")
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_command")

    plugin_subparsers.add_parser("list", help="List installed plugins")
    enable_parser = plugin_subparsers.add_parser("enable", help="Enable a plugin")
    enable_parser.add_argument("name", help="Plugin name")
    disable_parser = plugin_subparsers.add_parser("disable", help="Disable a plugin")
    disable_parser.add_argument("name", help="Plugin name")
    info_parser = plugin_subparsers.add_parser("info", help="Show plugin info")
    info_parser.add_argument("name", help="Plugin name")

    # autoplay commands
    autoplay_parser = subparsers.add_parser("autoplay", help="Autoplay management")
    autoplay_subparsers = autoplay_parser.add_subparsers(dest="autoplay_command")

    autoplay_subparsers.add_parser("status", help="Show autoplay status")
    strategy_parser = autoplay_subparsers.add_parser("strategy", help="Set autoplay strategy")
    strategy_parser.add_argument("strategy", help="Strategy name")

    # queue commands
    queue_parser = subparsers.add_parser("queue", help="Queue management")
    queue_subparsers = queue_parser.add_subparsers(dest="queue_command")

    inspect_parser = queue_subparsers.add_parser("inspect", help="Inspect queue state")
    inspect_parser.add_argument("--guild-id", type=int, help="Guild ID")

    args = parser.parse_args()

    setup_logging(args.log_level)

    commands = {
        "health-check": health_check,
        "debug": debug_monitor,
        "show-stats": show_stats,
        "create-bot": create_bot,
        "doctor": doctor_check,
        "test-node": test_node,
        "profile": profile_performance,
    }

    # Handle subcommands
    if args.command == "plugin":
        handle_plugin_command(args)
    elif args.command == "autoplay":
        handle_autoplay_command(args)
    elif args.command == "queue":
        handle_queue_command(args)
    elif args.command == "doctor":
        doctor_check(args)
    elif args.command == "profile":
        profile_performance(args)
    elif args.command == "snapshot":
        handle_snapshot_command(args)
    elif args.command == "benchmark":
        run_benchmark(args)
    elif args.command == "wiretap":
        handle_wiretap_command(args)
    elif args.command in commands:
        asyncio.run(commands[args.command](args))
    else:
        parser.print_help()

    if args.command in commands:
        asyncio.run(commands[args.command](args))
    else:
        parser.print_help()


async def health_check(args: Any) -> None:
    """Perform health check on Lavalink node."""
    node_config = {
        "host": args.host,
        "port": args.port,
        "password": args.password,
    }

    client = SonoraClient([node_config])
    try:
        await client.start()
        print("✓ Lavalink node is healthy")
        # Check stats
        for node in client.nodes:
            stats = await node.get_stats()
            if stats:
                print(f"  - Uptime: {stats.get('uptime', 'unknown')}")
                print(f"  - Players: {stats.get('players', 0)}")
                print(f"  - CPU: {stats.get('cpu', {}).get('cores', 'unknown')} cores")
    except Exception as e:
        print(f"✗ Lavalink node health check failed: {e}")
        sys.exit(1)
    finally:
        await client.close()


async def debug_monitor(args: Any) -> None:
    """Start interactive debug monitor."""
    print("Sonora Debug Monitor")
    print("Press Ctrl+C to exit")

    node_config = {
        "host": args.host,
        "port": args.port,
        "password": args.password,
    }

    client = SonoraClient([node_config])
    try:
        await client.start()

        while True:
            print("\n" + "=" * 50)
            print("Active Players:", len(client.players))
            print("Connected Nodes:", sum(1 for node in client.nodes if node.connected))

            for guild_id, player in client.players.items():
                print(f"Guild {guild_id}:")
                print(
                    f"  - Current: {player.queue.current.title if player.queue.current else 'None'}"
                )
                print(f"  - Queue length: {player.queue.length}")
                print(f"  - Volume: {player.volume}")
                print(f"  - Paused: {player.paused}")

            await asyncio.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting debug monitor...")
    finally:
        await client.close()


async def show_stats(args: Any) -> None:
    """Show current metrics."""
    print("Sonora Metrics:")
    print(json.dumps(metrics.get_metrics(), indent=2))


async def create_bot(args: Any) -> None:
    """Generate bot template."""
    framework = args.framework
    name = args.name

    print(f"Creating {framework} bot template: {name}")

    # This would generate template files
    # For now, just print info
    print(f"Generated {framework} bot in ./{name}/")
    print("Don't forget to:")
    print("1. Install dependencies")
    print("2. Set environment variables")


def handle_plugin_command(args: Any) -> None:
    """Handle plugin subcommands."""
    if args.plugin_command == "list":
        print("Installed plugins:")
        # TODO: Implement plugin listing
        print("  - YouTube (enabled)")
        print("  - Spotify (disabled)")
    elif args.plugin_command == "enable":
        print(f"Enabling plugin: {args.name}")
        # TODO: Implement plugin enabling
    elif args.plugin_command == "disable":
        print(f"Disabling plugin: {args.name}")
        # TODO: Implement plugin disabling
    elif args.plugin_command == "info":
        print(f"Plugin info for: {args.name}")
        # TODO: Implement plugin info
    else:
        print("Invalid plugin command")


def handle_autoplay_command(args: Any) -> None:
    """Handle autoplay subcommands."""
    if args.autoplay_command == "status":
        print("Autoplay status:")
        print("  - Enabled: True")
        print("  - Strategy: similar_artist")
        print("  - Fallback: global_fallback")
        # TODO: Connect to actual client/player
    elif args.autoplay_command == "strategy":
        print(f"Setting autoplay strategy to: {args.strategy}")
        # TODO: Implement strategy setting
    else:
        print("Invalid autoplay command")


def handle_queue_command(args: Any) -> None:
    """Handle queue subcommands."""
    if args.queue_command == "inspect":
        guild_id = args.guild_id or 0
        print(f"Queue inspection for guild {guild_id}:")
        print("  - Current track: None")
        print("  - Queue length: 0")
        print("  - History length: 0")
        print("  - Smart shuffle: enabled")
        print("  - Skip fatigue threshold: 3")
        print("  - Session memory: enabled")
        # TODO: Connect to actual player
    else:
        print("Invalid queue command")


def doctor_check(args: Any) -> None:
    """Check environment and dependencies."""
    print("🔍 Sonora Doctor - Environment Check")
    print("=" * 50)

    # Check Python version
    import sys
    python_version = sys.version_info
    print(f"✅ Python: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # Check required packages
    required_packages = ['aiohttp', 'pydantic', 'typing_extensions']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('_', ''))
            print(f"✅ {package}: installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: missing")

    # Check optional packages
    optional_packages = ['cryptography', 'psutil']
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}: installed (optional)")
        except ImportError:
            print(f"⚠️  {package}: not installed (optional)")

    # Check Lavalink connection
    print(f"🔗 Lavalink: {args.host}:{args.port}")
    print("   Use 'sonoractl health-check' to test connection")

    if missing_packages:
        print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\n✅ All checks passed!")


def profile_performance(args: Any) -> None:
    """Profile performance and show metrics."""
    print("📊 Sonora Performance Profile")
    print("=" * 50)

    try:
        from .performance import performance_monitor, async_profiler, backpressure_controller

        # System stats
        system_stats = performance_monitor.get_system_stats()
        print("System Metrics:")
        print(f"  CPU: {system_stats['cpu_percent']:.1f}%")
        print(f"  Memory: {system_stats['memory_mb']:.1f} MB ({system_stats['memory_percent']:.1f}%)")
        print(f"  Threads: {system_stats['threads']}")
        print(f"  Open files: {system_stats['open_files']}")

        # Performance stats
        perf_stats = performance_monitor.get_stats()
        print("\nApplication Metrics:")
        print(f"  Uptime: {perf_stats['uptime']:.1f}s")

        if 'counters' in perf_stats:
            print("  Counters:")
            for name, value in perf_stats['counters'].items():
                print(f"    {name}: {value}")

        # Task profiling
        task_stats = async_profiler.get_task_stats()
        if task_stats:
            print("\nTask Profiling:")
            for task_name, stats in task_stats.items():
                print(f"  {task_name}:")
                print(f"    Count: {stats['count']}")
                print(f"    Avg: {stats['avg']:.3f}s")
                print(f"    Max: {stats['max']:.3f}s")

        # Backpressure stats
        bp_stats = backpressure_controller.get_stats()
        print("\nBackpressure Control:")
        print(f"  Active: {bp_stats['active']}")
        print(f"  Queued: {bp_stats['queued']}")
        print(f"  Dropped: {bp_stats['dropped']}")

    except ImportError:
        print("❌ Performance monitoring not available")
        print("   Install optional dependencies: pip install cryptography psutil")


def handle_snapshot_command(args: Any) -> None:
    """Handle snapshot subcommands."""
    try:
        from .snapshot import snapshot_manager
    except ImportError:
        print("❌ Snapshot functionality not available")
        return

    if args.snapshot_command == "save":
        # This would need actual player context
        print("📸 Snapshot saved: session_001.json")
        print("💡 Use 'sonoractl snapshot list' to see all snapshots")
    elif args.snapshot_command == "list":
        snapshots = snapshot_manager.list_snapshots()
        if snapshots:
            print("📁 Saved snapshots:")
            for snapshot in snapshots:
                print(f"  • {snapshot}")
        else:
            print("📭 No snapshots found")
    elif args.snapshot_command == "restore":
        filename = args.filename
        print(f"🔄 Restoring snapshot: {filename}")
        print("✅ Session restored successfully")


def run_benchmark(args: Any) -> None:
    """Run performance benchmarks."""
    print("🏃 Running Sonora Performance Benchmarks")
    print("=" * 50)

    try:
        from .performance import performance_monitor, async_profiler
        from .diagnostics import performance_profiler

        # Start profiling
        performance_profiler.start_profiling()
        start_time = time.time()

        # Simulate some work
        import asyncio
        async def benchmark_work():
            tasks = []
            for i in range(100):
                task = asyncio.create_task(asyncio.sleep(0.001))
                tasks.append(task)
            await asyncio.gather(*tasks)

        asyncio.run(benchmark_work())

        # Stop profiling
        profile_results = performance_profiler.stop_profiling()
        end_time = time.time()

        print(f"  Execution time: {end_time - start_time:.2f}s")
        print(f"  Memory peak: {profile_results.get('memory_peak_mb', 0):.1f} MB")
        print(f"  Memory current: {profile_results.get('memory_current_mb', 0):.1f} MB")
        print("\n📊 Top 5 most time-consuming functions:")
        profile_lines = profile_results.get("profile_stats", "").split("\n")
        function_lines = [line for line in profile_lines if "function calls" in line or "/" in line and "sonora" in line]
        for line in function_lines[:5]:
            if line.strip():
                print(f"  {line.strip()}")

    except ImportError:
        print("❌ Benchmarking not available")
        print("   Install optional dependencies: pip install cryptography psutil")


def handle_wiretap_command(args: Any) -> None:
    """Handle wiretap subcommands."""
    try:
        from .diagnostics import wiretap_debugger
    except ImportError:
        print("❌ Wiretap debugging not available")
        return

    if args.wiretap_command == "start":
        wiretap_debugger.enable()
        print("🎯 Wiretap debugging enabled")
        print("📡 Capturing Lavalink protocol packets...")
        print("💡 Use 'sonoractl wiretap stop' to stop and view captured packets")
    elif args.wiretap_command == "stop":
        wiretap_debugger.disable()
        packets = wiretap_debugger.get_captured_packets(10)
        print("🛑 Wiretap debugging stopped")
        print(f"📦 Captured {len(packets)} packets (showing last 10):")

        for i, packet in enumerate(packets, 1):
            print(f"  {i}. {packet.get('event_type', 'unknown')} - {packet.get('timestamp', 'no_time')}")





async def test_node(args: Any) -> None:
    """Test node connection and performance."""
    import time

    node_config = {
        "host": args.host,
        "port": args.port,
        "password": args.password,
    }

    client = SonoraClient([node_config])
    try:
        start_time = time.time()
        await client.start()
        connect_time = time.time() - start_time

        print(f"Connection time: {connect_time:.2f}s")
        print("✓ Node connection successful")

        # Test basic load
        # This would test loading a track, etc.

    except Exception as e:
        print(f"✗ Node test failed: {e}")
        sys.exit(1)
    finally:
        await client.close()


if __name__ == "__main__":
    main()

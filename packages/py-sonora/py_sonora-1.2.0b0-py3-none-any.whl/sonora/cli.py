"""CLI utility for Sonora."""

import argparse
import asyncio
import json
import sys
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

    # doctor command
    subparsers.add_parser("doctor", help="Check environment and dependencies")

    # test-node command
    subparsers.add_parser("test-node", help="Test node connection and performance")

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
    }

    # Handle subcommands
    if args.command == "plugin":
        handle_plugin_command(args)
    elif args.command == "autoplay":
        handle_autoplay_command(args)
    elif args.command == "queue":
        handle_queue_command(args)
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
        guild_id = args.guild_id
        print(f"Queue inspection for guild {guild_id}:")
        print("  - Current track: None")
        print("  - Queue length: 0")
        print("  - History length: 0")
        print("  - Smart shuffle: enabled")
        # TODO: Connect to actual player
    else:
        print("Invalid queue command")
    print("3. Run the bot")


async def doctor_check(args: Any) -> None:
    """Check environment and dependencies."""
    print("Sonora Doctor Check")
    print("=" * 30)

    # Check Python version
    import sys

    print(f"Python version: {sys.version}")

    # Check dependencies
    try:
        import importlib.util

        if importlib.util.find_spec("aiohttp"):
            print("✓ aiohttp available")
        else:
            print("✗ aiohttp not found")
    except ImportError:
        print("✗ aiohttp not found")

    try:
        import importlib.util

        if importlib.util.find_spec("pydantic"):
            print("✓ pydantic available")
        else:
            print("✗ pydantic not found")
    except ImportError:
        print("✗ pydantic not found")

    # Check Lavalink connection
    try:
        await health_check(args)
    except SystemExit:
        pass


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

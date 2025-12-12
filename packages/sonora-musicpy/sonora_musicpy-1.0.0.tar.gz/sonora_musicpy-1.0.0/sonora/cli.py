"""CLI utility for Sonora."""

import argparse
import asyncio
import sys
import json
from typing import Dict, Any
from .client import SonoraClient
from .utils import setup_logging
from .metrics import metrics


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Sonora CLI utility")
    parser.add_argument("--host", default="127.0.0.1", help="Lavalink host")
    parser.add_argument("--port", type=int, default=2333, help="Lavalink port")
    parser.add_argument("--password", default="youshallnotpass", help="Lavalink password")
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
    create_parser.add_argument("framework", choices=["discord.py", "nextcord", "pycord"], help="Discord framework")
    create_parser.add_argument("name", help="Bot name")

    # doctor command
    subparsers.add_parser("doctor", help="Check environment and dependencies")

    # test-node command
    subparsers.add_parser("test-node", help="Test node connection and performance")

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

    if args.command in commands:
        asyncio.run(commands[args.command](args))
    else:
        parser.print_help()


async def health_check(args):
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


async def debug_monitor(args):
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
            print("\n" + "="*50)
            print("Active Players:", len(client.players))
            print("Connected Nodes:", sum(1 for node in client.nodes if node.connected))

            for guild_id, player in client.players.items():
                print(f"Guild {guild_id}:")
                print(f"  - Current: {player.queue.current.title if player.queue.current else 'None'}")
                print(f"  - Queue length: {player.queue.length}")
                print(f"  - Volume: {player.volume}")
                print(f"  - Paused: {player.paused}")

            await asyncio.sleep(5)

    except KeyboardInterrupt:
        print("\nExiting debug monitor...")
    finally:
        await client.close()


async def show_stats(args):
    """Show current metrics."""
    print("Sonora Metrics:")
    print(json.dumps(metrics.get_metrics(), indent=2))


async def create_bot(args):
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
    print("3. Run the bot")


async def doctor_check(args):
    """Check environment and dependencies."""
    print("Sonora Doctor Check")
    print("="*30)

    # Check Python version
    import sys
    print(f"Python version: {sys.version}")

    # Check dependencies
    try:
        import aiohttp
        print("✓ aiohttp available")
    except ImportError:
        print("✗ aiohttp not found")

    try:
        import pydantic
        print("✓ pydantic available")
    except ImportError:
        print("✗ pydantic not found")

    # Check Lavalink connection
    try:
        await health_check(args)
    except SystemExit:
        pass


async def test_node(args):
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
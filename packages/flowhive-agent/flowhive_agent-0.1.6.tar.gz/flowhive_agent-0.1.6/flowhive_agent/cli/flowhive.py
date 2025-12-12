"""
Unified CLI entry point for FlowHive agent.
Supports 'config' and 'run' subcommands, similar to git.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from urllib.parse import urljoin

AGENT_ROOT = Path(__file__).resolve().parents[1]
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from core.config import (
    apply_overrides,
    get_config_value,
    list_config,
    load_config,
    set_config_value,
)
from core.control_plane import (
    ControlPlaneClient,
    ControlPlaneConfig,
    ControlPlaneEventPublisher,
    TaskLogStreamer,
    TaskStatusReporter,
)
from core.manager import TaskManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FlowHive Agent - Distributed task execution agent",
        prog="flowhive",
        epilog="""Examples:
  # List all configuration
  flowhive config
  
  # Set user credentials
  flowhive config user.username myuser
  flowhive config user.email user@example.com
  flowhive config user.password mypassword
  
  # Set API key (alternative to username/password)
  flowhive config api_key your-api-key-here
  
  # Set control server URL
  flowhive config control_base_url https://flowhive.wangzixi.top
  
  # Run agent with default config
  flowhive run
  
  # Run agent with custom config file
  flowhive run --config /path/to/config.toml
  
  # Run agent with debug logging
  flowhive run --log-level DEBUG

For more information, visit: https://pypi.org/project/flowhive-agent/
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # config subcommand
    config_parser = subparsers.add_parser(
        "config",
        help="Get and set configuration options",
        description="""Manage FlowHive agent configuration.

Configuration Keys:
  user.username       - Account username for authentication
  user.email          - Account email for authentication
  user.password       - Account password for authentication
  api_key             - API key for authentication (alternative to username/password)
  agent_id            - Unique identifier for this agent
  control_base_url    - Control server base URL
  log_dir             - Directory for agent logs
  max_parallel        - Maximum parallel tasks (default: 2)
  event_buffer        - Event buffer size (default: 512)
  label               - Human-readable label for this agent

Authentication:
  You can authenticate using either:
  1. API Key: Set 'api_key'
  2. Username/Password: Set 'user.username', 'user.email', and 'user.password'
        """,
        epilog="""Examples:
  # List all configuration
  flowhive config
  
  # Get a specific value
  flowhive config user.username
  
  # Set a value
  flowhive config user.username myuser
  
  # Set value in specific config file
  flowhive config --config /path/to/config.toml user.email user@example.com
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    config_parser.add_argument(
        "--global",
        dest="global_",
        action="store_true",
        help="Use global config file (~/.config/flowhive-agent/config.toml)"
    )
    config_parser.add_argument(
        "--config",
        metavar="PATH",
        help="Path to config file"
    )
    config_parser.add_argument(
        "key",
        nargs="?",
        help="Configuration key to get or set"
    )
    config_parser.add_argument(
        "value",
        nargs="?",
        help="Configuration value to set (omit to get current value)"
    )
    
    # run subcommand
    run_parser = subparsers.add_parser(
        "run",
        help="Run FlowHive agent and connect to Control Server",
        description="""Start the FlowHive agent and connect to the Control Server.

The agent will:
  1. Load configuration from file or environment
  2. Authenticate with the Control Server
  3. Listen for and execute tasks
  4. Report task status and stream logs

Configuration Priority (highest to lowest):
  1. Command-line arguments
  2. Config file specified by --config
  3. Config file from FLOWHIVE_AGENT_CONFIG environment variable
  4. Default config file (~/.config/flowhive-agent/config.toml)
  5. System config file (/etc/flowhive-agent/config.toml)
        """,
        epilog="""Examples:
  # Run with default configuration
  flowhive run
  
  # Run with custom config file
  flowhive run --config /path/to/config.toml
  
  # Run with debug logging
  flowhive run --log-level DEBUG
  
  # Override control server URL
  flowhive run --control-base-url https://custom-server.example.com
  
  # Run with API key authentication
  flowhive run --api-key your-api-key-here
  
  # Run with custom agent ID and max parallel tasks
  flowhive run --agent-id my-agent-001 --max-parallel 4
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_parser.add_argument(
        "--config",
        metavar="PATH",
        help="Path to agent config file"
    )
    run_parser.add_argument(
        "--agent-id",
        metavar="ID",
        help="Override agent ID from config"
    )
    run_parser.add_argument(
        "--account-username",
        metavar="USERNAME",
        help="Override account username from config"
    )
    run_parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="Override API key from config (alternative to username/password)"
    )
    run_parser.add_argument(
        "--control-base-url",
        metavar="URL",
        help="Override Control Server base URL (e.g., https://control.flowhive.io)"
    )
    run_parser.add_argument(
        "--log-dir",
        metavar="DIR",
        help="Override log directory from config"
    )
    run_parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    run_parser.add_argument(
        "--max-parallel",
        type=int,
        metavar="N",
        help="Override maximum parallel tasks from config"
    )
    run_parser.add_argument(
        "--event-buffer",
        type=int,
        metavar="SIZE",
        help="Override event buffer size from config"
    )
    
    return parser


def to_ws_url(base_url: str, agent_id: str) -> str:
    url = base_url.rstrip("/")
    if url.startswith("https://"):
        url = "wss://" + url[len("https://") :]
    elif url.startswith("http://"):
        url = "ws://" + url[len("http://") :]
    # Use /api/v1 directly since agents connect to backend without proxy
    return urljoin(f"{url}/", f"api/ws/agents/{agent_id}")


def cmd_config(args: argparse.Namespace) -> int:
    """Handle config subcommand."""
    config_path = args.config if args.config else None
    
    if args.key is None:
        # List all config
        try:
            config_dict, conf = list_config(config_path)
            if not config_dict:
                print("No configuration found.", file=sys.stderr)
                print("\nTo create a new configuration, set values using:", file=sys.stderr)
                print("  flowhive config user.username <username>", file=sys.stderr)
                print("  flowhive config user.email <email>", file=sys.stderr)
                print("  flowhive config user.password <password>", file=sys.stderr)
                print("\nOr use API key authentication:", file=sys.stderr)
                print("  flowhive config api_key <your-api-key>", file=sys.stderr)
                return 1
            if conf:
                print(f"Configuration file: {conf}")
            else:
                print("Configuration: (using defaults)")
            print("Current configuration:")
            print()
            for key, value in sorted(config_dict.items()):
                # Mask sensitive values in display
                # if key in ("user.password", "api_key"):
                #     masked_value = "*" *  8 if value else "(not set)"
                #     print(f"  {key:20s} = {masked_value}")
                # else:
                #     print(f"  {key:20s} = {value}")
                print(f"  {key:20s} = {value}")
            return 0
        except Exception as e:
            print(f"Error reading configuration: {e}", file=sys.stderr)
            return 1
    
    if args.value is None:
        # Get config value
        try:
            value = get_config_value(args.key, config_path)
            if value is None:
                print(f"Error: Key '{args.key}' not found.", file=sys.stderr)
                print(f"\nAvailable keys:", file=sys.stderr)
                print("  user.username, user.email, user.password", file=sys.stderr)
                print("  api_key, agent_id, control_base_url", file=sys.stderr)
                print("  log_dir, max_parallel, event_buffer, label", file=sys.stderr)
                print(f"\nUse 'flowhive config' to list all current values.", file=sys.stderr)
                return 1
            print(value)
            return 0
        except Exception as e:
            print(f"Error reading configuration: {e}", file=sys.stderr)
            return 1
    
    # Set config value
    try:
        target = set_config_value(args.key, args.value, global_=args.global_, path=config_path)
        print(f"✓ Set {args.key} = {args.value}")
        if not args.config:
            print(f"✓ Configuration written to: {target}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(f"\nValid configuration keys:", file=sys.stderr)
        print("  user.username, user.email, user.password", file=sys.stderr)
        print("  api_key, agent_id, control_base_url", file=sys.stderr)
        print("  log_dir, max_parallel, event_buffer, label", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Error: Permission denied writing to config file.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error setting configuration: {e}", file=sys.stderr)
        print(f"\nPlease check:", file=sys.stderr)
        print(f"  - The config file path is valid", file=sys.stderr)
        print(f"  - You have write permissions", file=sys.stderr)
        print(f"  - The value format is correct", file=sys.stderr)
        return 1


async def async_run(args: argparse.Namespace) -> None:
    """Handle run subcommand."""
    try:
        base_config = load_config(args.config)
    except FileNotFoundError as exc:
        print(f"Error: Configuration file not found.", file=sys.stderr)
        print(f"Details: {exc}", file=sys.stderr)
        print(f"\nTo create a configuration file, run:", file=sys.stderr)
        print(f"  flowhive config user.username <username>", file=sys.stderr)
        print(f"  flowhive config user.email <email>", file=sys.stderr)
        print(f"  flowhive config user.password <password>", file=sys.stderr)
        print(f"  flowhive config control_base_url <url>", file=sys.stderr)
        print(f"\nOr specify a config file:", file=sys.stderr)
        print(f"  flowhive run --config /path/to/config.toml", file=sys.stderr)
        sys.exit(1)
    except KeyError as exc:
        print(f"Error: Invalid configuration file.", file=sys.stderr)
        print(f"Details: {exc}", file=sys.stderr)
        print(f"\nRequired fields: agent_id, control_base_url", file=sys.stderr)
        print(f"Authentication: Either api_key OR (user.username, user.email, user.password)", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Error: Failed to load configuration.", file=sys.stderr)
        print(f"Details: {exc}", file=sys.stderr)
        sys.exit(1)
    
    config = apply_overrides(base_config, args=args)
    
    # Validate required fields
    if not config.agent_id:
        print(f"Error: agent_id is required.", file=sys.stderr)
        print(f"Set it using: flowhive config agent_id <id>", file=sys.stderr)
        sys.exit(1)
    
    if not config.control_base_url:
        print(f"Error: control_base_url is required.", file=sys.stderr)
        print(f"Set it using: flowhive config control_base_url <url>", file=sys.stderr)
        sys.exit(1)
    
    # Check authentication: either api_key OR (account_email, account_password, account_username)
    if config.api_key:
        # API key authentication - no need for username/password
        print(f"✓ Using API key authentication")
    else:
        # Username/password authentication - need all three
        missing = []
        if not config.account_email:
            missing.append("user.email")
        if not config.account_password:
            missing.append("user.password")
        if not config.account_username:
            missing.append("user.username")
        if missing:
            print(f"Error: Missing required authentication configuration.", file=sys.stderr)
            print(f"Missing: {', '.join(missing)}", file=sys.stderr)
            print(f"\nYou must configure either:", file=sys.stderr)
            print(f"  1. API Key authentication:", file=sys.stderr)
            print(f"     flowhive config api_key <your-api-key>", file=sys.stderr)
            print(f"\n  2. Username/Password authentication:", file=sys.stderr)
            print(f"     flowhive config user.username <username>", file=sys.stderr)
            print(f"     flowhive config user.email <email>", file=sys.stderr)
            print(f"     flowhive config user.password <password>", file=sys.stderr)
            sys.exit(1)
        print(f"✓ Using username/password authentication for {config.account_username}")
    
    print(f"✓ Agent ID: {config.agent_id}")
    print(f"✓ Control Server: {config.control_base_url}")
    print(f"✓ Max parallel tasks: {config.max_parallel}")
    if config.label:
        print(f"✓ Agent label: {config.label}")
    print(f"\nStarting agent...")
    
    ws_url = to_ws_url(config.control_base_url, config.agent_id)
    loop = asyncio.get_running_loop()
    outbound: asyncio.Queue = asyncio.Queue(maxsize=config.event_buffer)
    publisher = ControlPlaneEventPublisher(loop, outbound)
    status_hook = TaskStatusReporter(publisher)
    log_streamer = TaskLogStreamer(publisher)
    
    manager = TaskManager(
        log_dir=config.log_dir,
        max_parallel=config.max_parallel,
        status_hook=status_hook,
        log_streamer=log_streamer,
    )
    
    client = ControlPlaneClient(
        ControlPlaneConfig(
            ws_url=ws_url,
            agent_id=config.agent_id,
            account_username=config.account_username,
            account_password=config.account_password,
            api_key=config.api_key,
            label=config.label,
        ),
        task_manager=manager,
        outbound_queue=outbound,
    )
    
    try:
        await client.run_forever()
    except ConnectionError as exc:
        print(f"\nError: Failed to connect to Control Server.", file=sys.stderr)
        print(f"Details: {exc}", file=sys.stderr)
        print(f"\nPlease check:", file=sys.stderr)
        print(f"  - Control Server URL is correct: {config.control_base_url}", file=sys.stderr)
        print(f"  - Control Server is running and accessible", file=sys.stderr)
        print(f"  - Network connectivity", file=sys.stderr)
        print(f"  - Firewall settings", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"\nError: Agent encountered an unexpected error.", file=sys.stderr)
        print(f"Details: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("\nShutting down agent...")
        manager.shutdown()
        print("✓ Agent stopped.")


def cmd_run(args: argparse.Namespace) -> int:
    """Handle run subcommand (synchronous wrapper)."""
    try:
        asyncio.run(async_run(args))
    except KeyboardInterrupt:
        print("\n\n✓ Agent stopped by user (Ctrl+C)")
        return 0
    except Exception as exc:
        print(f"\nFatal error: {exc}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = build_parser()
    
    # Handle no arguments - show help
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nQuick Start:")
        print("  1. Configure authentication:")
        print("     flowhive config user.username <username>")
        print("     flowhive config user.email <email>")
        print("     flowhive config user.password <password>")
        print("\n  2. Set control server URL:")
        print("     flowhive config control_base_url https://control.flowhive.io")
        print("\n  3. Run the agent:")
        print("     flowhive run")
        return 1
    
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse calls sys.exit on error, we catch it to return proper exit code
        return e.code if isinstance(e.code, int) else 1
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "config":
        return cmd_config(args)
    elif args.command == "run":
        log_level = getattr(logging, args.log_level, logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        return cmd_run(args)
    else:
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


"""
Main entry point for running cursor_cli as a module.

Usage:
    python -m cursor_cli [cursor-agent args...]

Or if installed with entry point:
    cursor-cli [cursor-agent args...]

Default (streaming mode):
    cursor-cli "your prompt"
    # Equivalent to:
    cursor-cli --output-format stream-json --stream-partial-output -p "your prompt"

Text mode:
    cursor-cli --text "your prompt"
    # Equivalent to:
    cursor-cli --output-format text -p "your prompt"

Danger mode (setup permissions):
    cursor-cli --danger
    # Creates ~/.cursor/cli-config.json with extended permissions (default)

    cursor-cli --danger /path/to/folder
    # Creates /path/to/folder/.cursor/cli-config.json with extended permissions
"""

import sys
import os
import json
import argparse
from pathlib import Path
from .runner import CursorCLIRunner


# Default permissions to ensure in cli-config.json
DEFAULT_PERMISSIONS = {
    "allow": [
        "Shell(*)",
        "Read(*)",
        "Write(**/agents/**/*)",
        "Write(**/.agents/**/*)",
    ],
    "deny": [],
}

# cursor-agent subcommands that should be passed through without formatting
CURSOR_AGENT_SUBCOMMANDS = {
    "install-shell-integration",
    "uninstall-shell-integration",
    "login",
    "logout",
    "mcp",
    "status",
    "whoami",
    "update",
    "upgrade",
    "create-chat",
    "agent",
    "ls",
    "resume",
    "help",
}


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the runner."""
    parser = argparse.ArgumentParser(
        prog="cursor-cli",
        description="A wrapper for cursor-agent with formatted output support. "
        "Default mode is streaming with formatted output.",
        epilog="All unknown arguments are passed directly to cursor-agent.",
        add_help=False,  # We'll handle help ourselves to allow passthrough
    )

    # Runner-specific arguments
    runner_group = parser.add_argument_group("Runner Options")
    runner_group.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Prompt to send to cursor-agent (streaming mode by default)",
    )
    runner_group.add_argument(
        "--text",
        metavar="PROMPT",
        nargs="?",
        const="__TEXT_MODE__",
        help="Use text output mode instead of streaming. "
        "Equivalent to: --output-format text -p PROMPT",
    )
    runner_group.add_argument(
        "--danger",
        metavar="FOLDER_PATH",
        nargs="?",
        const="__DEFAULT_HOME__",
        help="Setup .cursor/cli-config.json with extended permissions. "
        "Default: ~/.cursor (user home directory)",
    )
    runner_group.add_argument(
        "--no-format",
        action="store_true",
        help="Disable formatted output for stream-json mode",
    )
    runner_group.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    runner_group.add_argument(
        "--runner-help", action="store_true", help="Show this help message and exit"
    )

    return parser


def setup_danger_permissions(folder_path: str) -> int:
    """
    Setup .cursor/cli-config.json with extended permissions.

    Args:
        folder_path: Path to the folder where .cursor directory will be created

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        folder = Path(folder_path).resolve()

        if not folder.exists():
            print(f"Error: Folder does not exist: {folder}")
            return 1

        if not folder.is_dir():
            print(f"Error: Path is not a directory: {folder}")
            return 1

        # Create .cursor directory
        cursor_dir = folder / ".cursor"
        cursor_dir.mkdir(exist_ok=True)

        # Config file path
        config_file = cursor_dir / "cli-config.json"

        # Load existing config or create new
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in {config_file}, creating new config")
                config = {}
        else:
            config = {}

        # Ensure permissions structure exists
        if "permissions" not in config:
            config["permissions"] = {}

        permissions = config["permissions"]

        # Ensure allow list exists
        if "allow" not in permissions:
            permissions["allow"] = []

        # Ensure deny list exists
        if "deny" not in permissions:
            permissions["deny"] = []

        # Append default permissions if not already present
        for perm in DEFAULT_PERMISSIONS["allow"]:
            if perm not in permissions["allow"]:
                permissions["allow"].append(perm)
                print(f"  Added permission: {perm}")

        # Write config back
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write("\n")

        print(f"✓ Updated {config_file}")
        print(f"\nCurrent permissions.allow:")
        for perm in permissions["allow"]:
            print(f"  - {perm}")

        return 0

    except PermissionError as e:
        print(f"Error: Permission denied: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def expand_args(runner_args, cursor_args: list) -> list:
    """
    Expand shorthand arguments to full cursor-agent arguments.

    Default (streaming):
        "prompt" expands to:
        --output-format stream-json --stream-partial-output -p "prompt"

    --text "prompt" expands to:
        --output-format text -p "prompt"
    """
    # Check if --text mode is requested
    if runner_args.text is not None:
        # Text mode
        expanded = ["--output-format", "text"]

        # Add prompt: either from --text value or from positional prompt
        if runner_args.text != "__TEXT_MODE__":
            expanded.extend(["-p", runner_args.text])
        elif runner_args.prompt:
            expanded.extend(["-p", runner_args.prompt])

        # Append any additional cursor args
        expanded.extend(cursor_args)
        return expanded

    # Default: streaming mode
    if runner_args.prompt:
        expanded = ["--output-format", "stream-json", "--stream-partial-output"]
        expanded.extend(["-p", runner_args.prompt])
        expanded.extend(cursor_args)
        return expanded

    # No prompt provided, just pass through cursor_args
    return cursor_args


def is_subcommand(argv: list) -> bool:
    """
    Check if the first argument is a cursor-agent subcommand.

    Args:
        argv: Command-line arguments

    Returns:
        True if the first argument is a subcommand
    """
    if not argv:
        return False
    first_arg = argv[0]
    # Check if it's a subcommand (not starting with -)
    if first_arg.startswith("-"):
        return False
    return first_arg in CURSOR_AGENT_SUBCOMMANDS


def main(argv: list | None = None) -> int:
    """
    Main entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code
    """
    if argv is None:
        argv = sys.argv[1:]

    # Check if this is a cursor-agent subcommand (pass through without formatting)
    if is_subcommand(argv):
        runner = CursorCLIRunner(use_colors=True)
        return runner.run(argv, format_output=False)

    # Parse our known arguments, passing rest to cursor-agent
    parser = create_parser()
    runner_args, cursor_args = parser.parse_known_args(argv)

    # Handle --danger mode
    if runner_args.danger is not None:
        # Default to user home directory if no path specified
        if runner_args.danger == "__DEFAULT_HOME__":
            folder_path = str(Path.home())
        else:
            folder_path = runner_args.danger
        return setup_danger_permissions(folder_path)

    # Show help if requested
    if runner_args.runner_help:
        parser.print_help()
        print("\n" + "=" * 60)
        print("Run 'cursor-agent --help' for cursor-agent specific options.")
        print("\nExamples:")
        print('  cursor-cli "Analyze this project"          # streaming mode (default)')
        print('  cursor-cli --text "Analyze this project"   # text mode')
        print('  cursor-cli --no-color "Hello"              # streaming without colors')
        print(
            '  cursor-cli --no-format "Hello"             # streaming without formatting'
        )
        print(
            "  cursor-cli --danger                        # setup permissions in ~/.cursor"
        )
        print(
            "  cursor-cli --danger /path/to/folder        # setup permissions in folder/.cursor"
        )
        return 0

    # Expand shorthand args
    cursor_args = expand_args(runner_args, cursor_args)

    # Show cursor-agent help if --help is in cursor_args
    if "--help" in cursor_args or "-h" in cursor_args:
        # Pass through to cursor-agent
        pass

    # If no arguments, show our help
    if not cursor_args:
        parser.print_help()
        print("\n" + "=" * 60)
        print("No arguments provided. Run 'cursor-agent --help' for options.")
        print("\nQuick start:")
        print('  cursor-cli "Your prompt here"')
        return 0

    # Create and run
    runner = CursorCLIRunner(use_colors=not runner_args.no_color)

    return runner.run(cursor_args, format_output=not runner_args.no_format)


if __name__ == "__main__":
    sys.exit(main())

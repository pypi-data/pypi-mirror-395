"""Main CLI entry point for fextapi."""

import argparse
import sys

from fextapi import __version__


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="fextapi",
        description="File-system based routing for FastAPI",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"fextapi v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    subparsers.add_parser("init", help="Initialize a new fextapi project")

    # Run command
    run_parser = subparsers.add_parser("run", help="Start the development server")
    run_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)"
    )
    run_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)"
    )
    run_parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload"
    )

    # Help command (handled automatically by argparse)
    subparsers.add_parser("help", help="Show this help message")

    # Version command (already handled by --version flag)
    subparsers.add_parser("version", help="Show version information")

    # Parse arguments
    args = parser.parse_args()

    # Handle commands
    if args.command == "init":
        from fextapi.cli.init import init_project
        init_project()

    elif args.command == "run":
        from fextapi.cli.run import run_server
        run_server(
            host=args.host,
            port=args.port,
            reload=not args.no_reload
        )

    elif args.command == "help":
        parser.print_help()

    elif args.command == "version":
        print(f"fextapi v{__version__}")

    else:
        # No command provided, show help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

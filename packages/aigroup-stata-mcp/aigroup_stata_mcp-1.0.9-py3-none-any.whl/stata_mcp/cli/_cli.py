#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import os
import sys
from importlib.metadata import version, PackageNotFoundError
from typing import Optional


def get_version() -> str:
    """Get the package version, handling cases where package is not installed."""
    try:
        return version("aigroup-stata-mcp")
    except PackageNotFoundError:
        # Fallback for development mode
        try:
            # Try to read from pyproject.toml
            import tomllib
            with open("pyproject.toml", "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "1.0.0-dev")
        except (FileNotFoundError, ImportError):
            return "1.0.0-dev"


def main() -> None:
    """Entry point for the command line interface."""
    parser = argparse.ArgumentParser(
        prog="aigroup-stata-mcp",
        description="Stata-MCP command line interface",
        add_help=True)
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Stata-MCP version is {get_version()}",
        help="show version information",
    )
    parser.add_argument(
        "-c", "--client",
        nargs="?",
        const="cc",
        help="set the client mode (default for Claude Code)"
    )
    parser.add_argument(
        "--usable",
        action="store_true",
        help="check whether Stata-MCP could be used on this computer",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="install Stata-MCP to Claude Desktop")
    parser.add_argument(
        "--config",
        type=str,
        help="path to configuration file (TOML format)")

    # mcp.run
    parser.add_argument(
        "-t",
        "--transport",
        choices=["stdio", "sse", "http", "streamable-http"],
        default=None,
        help="mcp server transport method (default: stdio)",
    )
    args = parser.parse_args()

    if args.usable:
        # Use absolute imports for installed package
        from stata_mcp.utils.usable import usable
        sys.exit(usable())

    elif args.install:
        from stata_mcp.utils.Installer import Installer
        Installer(sys_os=sys.platform).install()

    elif args.client:
        os.environ["STATA-MCP-CLIENT"] = "cc"
        from stata_mcp.server import run_server
        run_server(transport=args.transport or "stdio", config_path=args.config)

    else:
        from stata_mcp.server import run_server

        print("Starting Stata-MCP...")

        # Use stdio if there is no transport argument
        transport = args.transport or "stdio"
        if transport == "http":
            transport = (
                "streamable-http"  # Default to streamable-http for HTTP transport
            )
        run_server(transport=transport, config_path=args.config)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Main entry point for the Devici MCP Server.
"""

import logging
import sys


def setup_logging() -> None:
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main() -> None:
    """Main entry point that runs the server."""
    setup_logging()
    try:
        from .server import main as server_main
        server_main()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
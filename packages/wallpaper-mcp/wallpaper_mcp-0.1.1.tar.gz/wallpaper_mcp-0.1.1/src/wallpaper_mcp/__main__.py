"""Main entry point for wallpaper-mcp"""

import asyncio
from .server import main


def run():
    """CLI entry point"""
    asyncio.run(main())


if __name__ == "__main__":
    run()
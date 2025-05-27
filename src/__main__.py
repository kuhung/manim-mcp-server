"""Main entry point for the Manim MCP server package."""

import asyncio
from .server import main


if __name__ == "__main__":
    asyncio.run(main()) 
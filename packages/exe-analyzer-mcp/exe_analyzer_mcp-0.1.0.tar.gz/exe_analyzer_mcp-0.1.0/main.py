"""MCP server entry point for exe-analyzer-mcp."""

import asyncio
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from exe_analyzer_mcp.mcp_server import MCPServer


async def main():
    """Initialize and run the MCP server."""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

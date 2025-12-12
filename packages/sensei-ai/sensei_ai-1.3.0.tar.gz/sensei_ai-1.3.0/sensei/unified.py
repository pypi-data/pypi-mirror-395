"""Unified MCP server for Sensei.

Mounts all sub-servers into a single MCP endpoint:
- sensei_query, sensei_feedback (core)
- scout_glob, scout_read, scout_grep, scout_tree
- kura_search, kura_get
- tome_get, tome_search

Usage:
    from sensei import mcp
    mcp.run()  # stdio transport
    # or
    app = mcp.http_app(path="/mcp")  # HTTP transport
"""

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from sensei.kura import mcp as kura_mcp
from sensei.scout import mcp as scout_mcp
from sensei.server import mcp as sensei_mcp
from sensei.tome import mcp as tome_mcp


@asynccontextmanager
async def lifespan(server):
    """Ensure database is ready before handling MCP requests."""
    from sensei.database.local import ensure_db_ready

    await ensure_db_ready()
    yield


# Create unified MCP server
mcp = FastMCP(name="sensei", lifespan=lifespan)

# Mount all sub-servers with prefixes
mcp.mount(sensei_mcp, prefix="sensei")
mcp.mount(scout_mcp, prefix="scout")
mcp.mount(kura_mcp, prefix="kura")
mcp.mount(tome_mcp, prefix="tome")

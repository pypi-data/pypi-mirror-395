"""MCP (Model Context Protocol) server for mesh-toolkit.

This module provides an MCP server that exposes mesh-toolkit's 3D generation
capabilities to any MCP-compatible client (Claude Desktop, etc.).

Usage:
    # As a module
    python -m mesh_toolkit.agent_tools.mcp

    # Or programmatically
    from mesh_toolkit.agent_tools.mcp import create_server, run_server

    server = create_server()
    run_server(server)

Configuration:
    Set MESHY_API_KEY environment variable for API access.

    Optional:
    - MESH_TOOLKIT_MCP_PORT: Server port (default: 3000)
    - MESH_TOOLKIT_MCP_HOST: Server host (default: localhost)

Requirements:
    pip install mesh-toolkit[mcp]

    The MCP extra includes:
    - mcp (Model Context Protocol SDK)
"""

from mesh_toolkit.agent_tools.mcp.provider import (
    MCPToolProvider,
    create_server,
    run_server,
)

__all__ = [
    "MCPToolProvider",
    "create_server",
    "run_server",
]

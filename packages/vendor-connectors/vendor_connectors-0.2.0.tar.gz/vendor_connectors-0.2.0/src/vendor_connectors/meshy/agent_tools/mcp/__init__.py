"""MCP (Model Context Protocol) server for mesh-toolkit.

This module provides an MCP server that exposes mesh-toolkit's 3D generation
capabilities to any MCP-compatible client (Claude Desktop, etc.).

Usage:
    # As a module
    python -m vendor_connectors.meshy.agent_tools.mcp

    # Or programmatically
    from vendor_connectors.meshy.agent_tools.mcp import create_server, run_server

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

from __future__ import annotations

from vendor_connectors.meshy.agent_tools.mcp.provider import (
    MCPToolProvider,
    create_server,
    run_server,
)

__all__ = [
    "MCPToolProvider",
    "create_server",
    "run_server",
]

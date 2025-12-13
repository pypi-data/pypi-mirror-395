"""Agent tools for mesh-toolkit - AI agent integrations for 3D asset generation.

This subpackage provides integrations with various AI agent frameworks:
- CrewAI tools
- MCP (Model Context Protocol) server
- Future: Langchain, Autogen, etc.

Architecture:
    agent_tools/
        __init__.py          # This file - registry and exports
        base.py              # Base classes and interfaces
        registry.py          # Tool provider registry
        crewai/              # CrewAI-specific tools
        mcp/                 # MCP server implementation

Usage:
    # CrewAI integration
    from vendor_connectors.meshy.agent_tools.crewai import get_tools
    tools = get_tools()

    # MCP server
    from vendor_connectors.meshy.agent_tools.mcp import create_server
    server = create_server()

    # Registry for all providers
    from vendor_connectors.meshy.agent_tools import get_provider, list_providers
"""

from __future__ import annotations

from vendor_connectors.meshy.agent_tools.registry import (
    ToolProvider,
    get_provider,
    list_providers,
    register_provider,
)

__all__ = [
    "ToolProvider",
    "get_provider",
    "list_providers",
    "register_provider",
]

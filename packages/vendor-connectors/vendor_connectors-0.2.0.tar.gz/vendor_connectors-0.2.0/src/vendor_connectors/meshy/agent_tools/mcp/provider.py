"""MCP tool provider implementation.

This module creates an MCP server that exposes mesh-toolkit tools
to any MCP-compatible client.
"""

from __future__ import annotations

import json
from typing import Any

# Import to register tools
import vendor_connectors.meshy.agent_tools.tools  # noqa: F401
from vendor_connectors.meshy.agent_tools.base import (
    BaseToolProvider,
    get_tool_definition,
    get_tool_definitions,
)


class MCPToolProvider(BaseToolProvider):
    """MCP tool provider for mesh-toolkit.

    Creates an MCP server with tools for 3D asset generation.

    Usage:
        provider = MCPToolProvider()
        server = provider.create_server()
        provider.run(server)
    """

    def __init__(self):
        self._server = None
        self._tools: list[Any] = []
        self._tools_by_name: dict[str, Any] = {}

    @property
    def name(self) -> str:
        return "mcp"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_tools(self) -> list[Any]:
        """Get all tools as MCP tool definitions.

        Returns:
            List of MCP tool objects
        """
        if not self._tools:
            self._tools = self._create_mcp_tools()
            self._tools_by_name = {t.name: t for t in self._tools}
        return self._tools

    def get_tool(self, name: str) -> Any | None:
        """Get a specific tool by name (O(1) lookup)."""
        if not self._tools:
            self.get_tools()  # Ensure tools are loaded
        return self._tools_by_name.get(name)

    def _create_mcp_tools(self) -> list[Any]:
        """Create MCP tool definitions from our tool registry."""
        try:
            from mcp.types import Tool
        except ImportError:
            return []

        tools = []
        for definition in get_tool_definitions():
            # Convert parameters to JSON schema
            properties = {}
            required = []

            for param_name, param in definition.parameters.items():
                prop = {
                    "type": _python_type_to_json_schema(param.type),
                    "description": param.description,
                }

                if param.default is not None:
                    prop["default"] = param.default

                if param.enum_values:
                    prop["enum"] = param.enum_values

                properties[param_name] = prop

                if param.required:
                    required.append(param_name)

            tool = Tool(
                name=definition.name,
                description=definition.description,
                inputSchema={
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            )
            tools.append(tool)

        return tools

    def create_server(self):
        """Create and configure the MCP server.

        Returns:
            Configured MCP Server instance
        """
        try:
            from mcp.server import Server
        except ImportError as e:
            msg = "MCP SDK not installed. Install with: pip install mesh-toolkit[mcp]"
            raise ImportError(msg) from e

        server = Server("mesh-toolkit")

        # Register tools
        @server.list_tools()
        async def list_tools():
            return self.get_tools()

        # Handle tool calls
        @server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[Any]:
            from mcp.types import TextContent

            definition = get_tool_definition(name)
            if not definition:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": f"Unknown tool: {name}"}),
                    )
                ]

            try:
                result = definition.handler(**arguments)
                return [TextContent(type="text", text=result)]
            except Exception as e:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": str(e)}),
                    )
                ]

        self._server = server
        return server

    def run(self, server=None):
        """Run the MCP server.

        Args:
            server: Optional server instance (creates one if not provided)
        """
        import asyncio

        try:
            from mcp.server.stdio import stdio_server
        except ImportError as e:
            msg = "MCP SDK not installed. Install with: pip install mesh-toolkit[mcp]"
            raise ImportError(msg) from e

        if server is None:
            server = self.create_server()

        async def main():
            async with stdio_server() as (read_stream, write_stream):
                await server.run(
                    read_stream,
                    write_stream,
                    server.create_initialization_options(),
                )

        asyncio.run(main())


def _python_type_to_json_schema(python_type: type) -> str:
    """Convert Python type to JSON Schema type."""
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }
    return type_map.get(python_type, "string")


# Module-level convenience functions
_provider: MCPToolProvider | None = None


def _get_provider() -> MCPToolProvider:
    """Get or create the singleton provider."""
    global _provider
    if _provider is None:
        _provider = MCPToolProvider()
    return _provider


def create_server():
    """Create an MCP server with mesh-toolkit tools.

    Usage:
        from vendor_connectors.meshy.agent_tools.mcp import create_server

        server = create_server()

    Returns:
        Configured MCP Server instance
    """
    return _get_provider().create_server()


def run_server(server=None):
    """Run the MCP server.

    Args:
        server: Optional server instance (creates one if not provided)
    """
    _get_provider().run(server)

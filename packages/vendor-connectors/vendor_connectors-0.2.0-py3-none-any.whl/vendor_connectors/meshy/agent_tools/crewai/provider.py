"""CrewAI tool provider implementation.

This module converts mesh-toolkit's generic tool definitions into
CrewAI-compatible BaseTool instances.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

# Import to register tools
import vendor_connectors.meshy.agent_tools.tools  # noqa: F401
from vendor_connectors.meshy.agent_tools.base import (
    BaseToolProvider,
    ToolDefinition,
    get_tool_definitions,
)


def _create_pydantic_model(definition: ToolDefinition) -> type[BaseModel]:
    """Create a Pydantic model from a tool definition's parameters."""
    fields = {}

    for param_name, param in definition.parameters.items():
        field_kwargs = {"description": param.description}

        if not param.required:
            field_kwargs["default"] = param.default

        fields[param_name] = (param.type, Field(**field_kwargs))

    # Create dynamic Pydantic model
    return type(
        f"{definition.name.title().replace('_', '')}Input",
        (BaseModel,),
        {
            "__annotations__": {k: v[0] for k, v in fields.items()},
            **{k: v[1] for k, v in fields.items()},
        },
    )


def _create_tool_class(definition: ToolDefinition) -> type:
    """Create a CrewAI BaseTool class from a tool definition."""
    # Lazy import CrewAI
    from crewai.tools import BaseTool

    # Create input schema
    input_model = _create_pydantic_model(definition)

    # Create the tool class
    class_attrs = {
        "name": definition.name,
        "description": definition.description,
        "args_schema": input_model,
    }

    # Create _run method that calls the handler
    handler = definition.handler

    def _run(self, **kwargs) -> str:
        return handler(**kwargs)

    class_attrs["_run"] = _run

    # Create and return the class
    tool_class = type(
        f"{definition.name.title().replace('_', '')}Tool",
        (BaseTool,),
        class_attrs,
    )

    return tool_class


class CrewAIToolProvider(BaseToolProvider):
    """CrewAI tool provider for mesh-toolkit.

    Converts generic tool definitions into CrewAI BaseTool instances.

    Usage:
        provider = CrewAIToolProvider()
        tools = provider.get_tools()

        # Use with Agent
        agent = Agent(role="Artist", tools=tools, ...)
    """

    def __init__(self):
        self._tool_classes: dict[str, type] = {}
        self._tool_instances: dict[str, Any] = {}

    @property
    def name(self) -> str:
        return "crewai"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _ensure_tools_created(self) -> None:
        """Create tool classes if not already done."""
        if self._tool_classes:
            return

        for definition in get_tool_definitions():
            try:
                tool_class = _create_tool_class(definition)
                self._tool_classes[definition.name] = tool_class
            except ImportError:
                # CrewAI not installed
                pass

    def get_tools(self) -> list[Any]:
        """Get all tools as CrewAI BaseTool instances.

        Returns:
            List of BaseTool instances
        """
        self._ensure_tools_created()

        tools = []
        for name, tool_class in self._tool_classes.items():
            if name not in self._tool_instances:
                self._tool_instances[name] = tool_class()
            tools.append(self._tool_instances[name])

        return tools

    def get_tool(self, name: str) -> Any | None:
        """Get a specific tool by name.

        Args:
            name: Tool name (e.g., 'text3d_generate')

        Returns:
            BaseTool instance or None
        """
        self._ensure_tools_created()

        if name not in self._tool_classes:
            return None

        if name not in self._tool_instances:
            self._tool_instances[name] = self._tool_classes[name]()

        return self._tool_instances[name]

    def get_tool_class(self, name: str) -> type | None:
        """Get a tool class (not instance) by name.

        Useful when you want to create multiple instances with different configs.

        Args:
            name: Tool name

        Returns:
            Tool class or None
        """
        self._ensure_tools_created()
        return self._tool_classes.get(name)


# Module-level convenience functions
_provider: CrewAIToolProvider | None = None


def _get_provider() -> CrewAIToolProvider:
    """Get or create the singleton provider."""
    global _provider
    if _provider is None:
        _provider = CrewAIToolProvider()
    return _provider


def get_tools() -> list[Any]:
    """Get all mesh-toolkit tools as CrewAI BaseTool instances.

    Usage:
        from vendor_connectors.meshy.agent_tools.crewai import get_tools

        tools = get_tools()
        agent = Agent(role="Artist", tools=tools, ...)

    Returns:
        List of BaseTool instances
    """
    return _get_provider().get_tools()


def get_tool(name: str) -> Any | None:
    """Get a specific tool by name.

    Args:
        name: Tool name (e.g., 'text3d_generate', 'list_animations')

    Returns:
        BaseTool instance or None if not found
    """
    return _get_provider().get_tool(name)

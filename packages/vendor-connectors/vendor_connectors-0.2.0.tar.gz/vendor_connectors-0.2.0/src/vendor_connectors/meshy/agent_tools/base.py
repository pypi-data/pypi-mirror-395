"""Base classes and interfaces for mesh-toolkit agent tools.

This module defines the abstract interfaces that all tool providers must implement,
enabling a consistent API across different agent frameworks (CrewAI, MCP, etc.).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


class ToolCategory(str, Enum):
    """Categories of mesh-toolkit tools."""

    GENERATION = "generation"  # Create new 3D assets
    RIGGING = "rigging"  # Add skeletons/rigs
    ANIMATION = "animation"  # Apply/manage animations
    TEXTURING = "texturing"  # Texture/retexture models
    UTILITY = "utility"  # Status checks, listings, etc.


@dataclass
class ToolDefinition:
    """Definition of a tool that can be exposed to agents.

    This is framework-agnostic - each provider converts this to their
    native tool format (CrewAI BaseTool, MCP Tool, etc.).

    Attributes:
        name: Unique tool identifier (snake_case)
        description: Human-readable description for agents
        category: Tool category for organization
        parameters: Dict of parameter name -> ParameterDefinition
        handler: The actual function that implements the tool
        requires_api_key: Whether MESHY_API_KEY is required
    """

    name: str
    description: str
    category: ToolCategory
    parameters: dict[str, ParameterDefinition]
    handler: Callable[..., str]
    requires_api_key: bool = True


@dataclass
class ParameterDefinition:
    """Definition of a tool parameter.

    Attributes:
        name: Parameter name
        description: Description for agents
        type: Python type (str, int, bool, etc.)
        required: Whether parameter is required
        default: Default value if not required
        enum_values: Optional list of allowed values
    """

    name: str
    description: str
    type: type
    required: bool = True
    default: Any = None
    enum_values: list[str] | None = None


@dataclass
class ToolResult:
    """Result from executing a tool.

    Attributes:
        success: Whether the tool executed successfully
        data: The result data (JSON-serializable)
        error: Error message if success is False
        task_id: Meshy task ID if applicable
    """

    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    task_id: str | None = None

    def to_json(self) -> str:
        """Serialize to JSON string."""
        import json

        return json.dumps(
            {
                "success": self.success,
                "data": self.data,
                "error": self.error,
                "task_id": self.task_id,
            },
            indent=2,
        )


class BaseToolProvider(ABC):
    """Abstract base class for tool providers.

    Each agent framework (CrewAI, MCP, etc.) implements this interface
    to provide framework-specific tool wrappers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'crewai', 'mcp')."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Provider version."""
        ...

    @abstractmethod
    def get_tools(self) -> list[Any]:
        """Get all tools in the framework's native format.

        Returns:
            List of framework-specific tool objects
        """
        ...

    @abstractmethod
    def get_tool(self, name: str) -> Any | None:
        """Get a specific tool by name.

        Args:
            name: Tool name

        Returns:
            Framework-specific tool object, or None if not found
        """
        ...

    def list_tools(self) -> list[str]:
        """List available tool names.

        Returns:
            List of tool names
        """
        return [t.name if hasattr(t, "name") else str(t) for t in self.get_tools()]


# Core tool definitions - framework-agnostic
TOOL_DEFINITIONS: dict[str, ToolDefinition] = {}


def register_tool(definition: ToolDefinition) -> None:
    """Register a tool definition."""
    TOOL_DEFINITIONS[definition.name] = definition


def get_tool_definitions() -> list[ToolDefinition]:
    """Get all registered tool definitions."""
    return list(TOOL_DEFINITIONS.values())


def get_tool_definition(name: str) -> ToolDefinition | None:
    """Get a specific tool definition by name."""
    return TOOL_DEFINITIONS.get(name)

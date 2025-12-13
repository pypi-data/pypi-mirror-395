"""CrewAI tool provider for mesh-toolkit.

This module provides CrewAI-compatible tools for 3D asset generation.

Usage:
    from vendor_connectors.meshy.agent_tools.crewai import get_tools

    # Get all tools
    tools = get_tools()

    # Use with CrewAI agent
    from crewai import Agent
    agent = Agent(
        role="3D Artist",
        tools=tools,
        ...
    )

    # Or get specific tools
    from vendor_connectors.meshy.agent_tools.crewai import (
        Text3DGenerateTool,
        ApplyAnimationTool,
        ListAnimationsTool,
    )

Requirements:
    pip install mesh-toolkit[crewai]
"""

from __future__ import annotations

from vendor_connectors.meshy.agent_tools.crewai.provider import (
    CrewAIToolProvider,
    get_tool,
    get_tools,
)

# Lazy imports for tool classes - only load when accessed
_tool_classes = {}


def __getattr__(name: str):
    """Lazy load tool classes."""
    tool_names = {
        "Text3DGenerateTool": "text3d_generate",
        "RigModelTool": "rig_model",
        "ApplyAnimationTool": "apply_animation",
        "RetextureModelTool": "retexture_model",
        "ListAnimationsTool": "list_animations",
        "CheckTaskStatusTool": "check_task_status",
        "GetAnimationTool": "get_animation",
    }

    if name in tool_names:
        if name not in _tool_classes:
            from vendor_connectors.meshy.agent_tools.base import get_tool_definition
            from vendor_connectors.meshy.agent_tools.crewai.provider import _create_tool_class

            definition = get_tool_definition(tool_names[name])
            if definition:
                _tool_classes[name] = _create_tool_class(definition)

        return _tool_classes.get(name)

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


__all__ = [
    "ApplyAnimationTool",
    "CheckTaskStatusTool",
    "CrewAIToolProvider",
    "GetAnimationTool",
    "ListAnimationsTool",
    "RetextureModelTool",
    "RigModelTool",
    # Tool classes (lazy loaded)
    "Text3DGenerateTool",
    "get_tool",
    "get_tools",
]

"""Tool provider registry for mesh-toolkit.

This module provides a registry pattern for managing multiple tool providers
(CrewAI, MCP, Langchain, etc.), enabling runtime discovery and selection.

Usage:
    from vendor_connectors.meshy.agent_tools import get_provider, list_providers

    # List available providers
    providers = list_providers()  # ['crewai', 'mcp']

    # Get a specific provider
    crewai = get_provider('crewai')
    tools = crewai.get_tools()

    # Register a custom provider
    register_provider(MyCustomProvider())
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vendor_connectors.meshy.agent_tools.base import BaseToolProvider


# Thread-safe registry
_registry: dict[str, BaseToolProvider] = {}
_registry_lock = threading.Lock()


class _ToolProviderMeta(type):
    """Metaclass for ToolProvider to enable attribute-style access."""

    def __getattr__(cls, name: str) -> BaseToolProvider:
        """Get a provider by attribute access (e.g., ToolProvider.crewai)."""
        if name.startswith("_"):
            msg = f"'{cls.__name__}' has no attribute '{name}'"
            raise AttributeError(msg)
        provider = get_provider(name)
        if provider is None:
            msg = f"Provider '{name}' not found. Available: {list_providers()}"
            raise AttributeError(msg)
        return provider


class ToolProvider(metaclass=_ToolProviderMeta):
    """Namespace for accessing registered tool providers.

    Usage:
        from vendor_connectors.meshy.agent_tools import ToolProvider

        # Access CrewAI provider
        tools = ToolProvider.crewai.get_tools()

        # Access MCP provider
        server = ToolProvider.mcp.create_server()

        # Get any registered provider by name
        custom = ToolProvider.my_custom_provider
    """

    @classmethod
    def get(cls, name: str) -> BaseToolProvider:
        """Get a provider by name.

        Args:
            name: Provider name ('crewai', 'mcp', etc.)

        Returns:
            The provider instance

        Raises:
            AttributeError: If provider not found
        """
        provider = get_provider(name)
        if provider is None:
            msg = f"Provider '{name}' not found. Available: {list_providers()}"
            raise AttributeError(msg)
        return provider


def register_provider(provider: BaseToolProvider) -> None:
    """Register a tool provider.

    Args:
        provider: The provider instance to register

    Raises:
        ValueError: If a provider with the same name is already registered
    """
    with _registry_lock:
        name = provider.name
        if name in _registry:
            msg = f"Provider '{name}' is already registered"
            raise ValueError(msg)
        _registry[name] = provider


def unregister_provider(name: str) -> bool:
    """Unregister a tool provider.

    Args:
        name: Provider name to unregister

    Returns:
        True if provider was unregistered, False if not found
    """
    with _registry_lock:
        if name in _registry:
            del _registry[name]
            return True
        return False


def get_provider(name: str) -> BaseToolProvider | None:
    """Get a registered provider by name.

    If the provider isn't registered yet, attempts to load it.

    Args:
        name: Provider name ('crewai', 'mcp', etc.)

    Returns:
        The provider instance, or None if not found/loadable
    """
    with _registry_lock:
        if name in _registry:
            return _registry[name]

    # Try to load the provider module
    provider = _lazy_load_provider(name)
    if provider:
        with _registry_lock:
            _registry[name] = provider

    return provider


def list_providers() -> list[str]:
    """List all available provider names.

    Returns:
        List of provider names (includes both registered and loadable)
    """
    # Known providers that can be loaded
    known = {"crewai", "mcp"}

    with _registry_lock:
        registered = set(_registry.keys())

    return sorted(known | registered)


def _lazy_load_provider(name: str) -> BaseToolProvider | None:
    """Attempt to lazy-load a provider by name.

    Args:
        name: Provider name

    Returns:
        Provider instance or None if loading fails
    """
    try:
        if name == "crewai":
            from vendor_connectors.meshy.agent_tools.crewai import CrewAIToolProvider

            return CrewAIToolProvider()
        elif name == "mcp":
            from vendor_connectors.meshy.agent_tools.mcp import MCPToolProvider

            return MCPToolProvider()
    except ImportError:
        # Provider dependencies not installed
        return None
    except Exception:
        # Other loading errors
        return None

    return None

"""
universal_agent.tools.registry

Manages the catalog of available tools.
"""

from __future__ import annotations

from typing import Any, Callable, Dict


class ToolRegistry:
    def __init__(self):
        self._local_registry: Dict[str, Callable[..., Any]] = {}

    def register_local(self, name: str, func: Callable[..., Any]) -> None:
        """Register a python function as a local tool."""
        self._local_registry[name] = func

    def get_local_tool(self, name: str) -> Callable[..., Any]:
        if name not in self._local_registry:
            raise KeyError(f"Local tool '{name}' not found in registry.")
        return self._local_registry[name]

    # Future: manage MCP clients and dynamic discovery/introspection


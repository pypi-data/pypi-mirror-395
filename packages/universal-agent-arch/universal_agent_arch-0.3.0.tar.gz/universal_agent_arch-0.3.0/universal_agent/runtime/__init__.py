"""
Runtime entrypoints, handlers, and dependency injection.

This module provides:
- API endpoints (api_app)
- CLI interface (cli_app)
- Node handlers (RouterHandler, ToolHandler, HumanHandler)
- Contract registry for dependency injection (ContractRegistry)
"""

from .api import app as api_app
from .handlers import HumanHandler, RouterHandler, ToolHandler
from .cli import app as cli_app
from .registry import (
    ContractRegistry,
    RegistrationError,
    ResolutionError,
    get_global_registry,
    set_global_registry,
)

__all__ = [
    # Apps
    "api_app",
    "cli_app",
    # Handlers
    "RouterHandler",
    "ToolHandler",
    "HumanHandler",
    # Registry
    "ContractRegistry",
    "RegistrationError",
    "ResolutionError",
    "get_global_registry",
    "set_global_registry",
]


"""
universal_agent.runtime.config

Dependency Injection (DI) helpers for the Universal Agent runtime.
Classes are loaded dynamically from string paths (e.g. via environment variables)
so users can swap implementations without touching core code.
"""

from __future__ import annotations

import importlib
import logging
import os
from typing import Optional, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ConfigError(Exception):
    """Raised when a configured class cannot be imported or validated."""


def load_class(path: str, expected_type: Type[T]) -> Type[T]:
    """
    Dynamically import a class from a string path like ``my_module.MyClass``.
    Verifies the class matches the expected type.
    """
    try:
        module_path, class_name = path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
    except (ValueError, ImportError, AttributeError) as exc:
        raise ConfigError(f"Could not load class '{path}': {exc}") from exc

    if not issubclass(cls, expected_type):
        raise ConfigError(f"Class '{path}' is not a subclass of {expected_type.__name__}")

    return cls


class RuntimeConfig:
    """Central configuration derived from environment variables."""

    @property
    def task_store_path(self) -> str:
        return os.getenv("UAA_TASK_STORE", "universal_agent.task.store.SQLTaskStore")

    @property
    def task_queue_path(self) -> str:
        return os.getenv("UAA_TASK_QUEUE", "universal_agent.task.queue.InMemoryTaskQueue")

    @property
    def llm_client_path(self) -> str:
        return os.getenv("UAA_LLM_CLIENT", "universal_agent.runtime.defaults.MockLLMClient")

    @property
    def database_url(self) -> str:
        return os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./local.db")

    @property
    def otel_endpoint(self) -> Optional[str]:
        return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

    @property
    def tool_executor_local_path(self) -> str:
        return os.getenv("UAA_TOOL_EXECUTOR_LOCAL", "universal_agent.runtime.defaults.MockToolExecutor")

    @property
    def tool_executor_mcp_path(self) -> str:
        return os.getenv("UAA_TOOL_EXECUTOR_MCP", "universal_agent.runtime.defaults.MockToolExecutor")


# Singleton instance for easy import
config = RuntimeConfig()

__all__ = ["ConfigError", "RuntimeConfig", "config", "load_class"]


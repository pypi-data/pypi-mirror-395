"""
universal_agent.contracts

Public interfaces (extension seams) for the Universal Agent Architecture.
External adapters must implement these interfaces to plug into the kernel.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from universal_agent.graph.state import GraphState


class ITaskStore(ABC):
    """
    Contract for durability.
    Implementations: Postgres, Redis, DynamoDB, FileSystem, etc.
    """

    @abstractmethod
    async def save_task(self, state: GraphState) -> None:
        """Persist the current state of a task."""

    @abstractmethod
    async def get_task(self, execution_id: str) -> Optional[GraphState]:
        """Retrieve a task by ID."""

    @abstractmethod
    async def list_active_tasks(self) -> List[GraphState]:
        """Enumerate tasks that are not terminal (useful for recovery)."""


class ITaskQueue(ABC):
    """
    Contract for async work distribution.
    Implementations: SQS, RabbitMQ, Redis PubSub, InMemory.
    """

    @abstractmethod
    async def enqueue(self, execution_id: str, priority: int = 0) -> None:
        """Push a task ID to be processed."""

    @abstractmethod
    async def dequeue(self) -> Optional[str]:
        """Pop the next task ID to process."""


class IToolExecutor(ABC):
    """
    Contract for capability execution.
    Implementations: MCP Client, Local Subprocess, AWS Lambda Invoke.
    """

    @abstractmethod
    async def execute(self, config: Dict[str, Any], arguments: Dict[str, Any]) -> Any:
        """Run the tool and return JSON-serializable output."""


class IRouterStrategy(ABC):
    """
    Contract for decision making.
    Implementations: OpenAI/Anthropic Client, Rule Engine, Random.
    """

    @abstractmethod
    async def select_model(self, context: Dict[str, Any], candidates: List[str]) -> str:
        """Choose the model identifier to use."""

    @abstractmethod
    async def select_tools(self, context: Dict[str, Any], available_tools: List[str]) -> List[str]:
        """Choose which tools to expose for the decision."""


__all__ = ["ITaskStore", "ITaskQueue", "IToolExecutor", "IRouterStrategy"]


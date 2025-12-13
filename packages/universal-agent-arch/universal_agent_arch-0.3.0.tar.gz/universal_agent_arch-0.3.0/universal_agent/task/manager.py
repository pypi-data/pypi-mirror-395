"""
universal_agent.task.manager

Business logic for managing agent lifecycles.
Wraps the ITaskStore and provides clean APIs for create/resume/list.
"""

import logging
import uuid
from typing import Optional

from universal_agent.graph.state import ExecutionStatus, GraphState
from universal_agent.task.store import ITaskStore

logger = logging.getLogger(__name__)


class TaskManager:
    """Facade for Task persistence and management."""

    def __init__(self, store: ITaskStore):
        self.store = store

    async def create_execution(self, graph_name: str, version: str, context: dict) -> GraphState:
        """Initialize a new execution (does not start running it)."""
        state = GraphState(
            execution_id=str(uuid.uuid4()),
            graph_name=graph_name,
            graph_version=version,
            context=context,
            status=ExecutionStatus.PENDING,
        )
        await self.store.save_task(state)
        return state

    async def get_execution(self, execution_id: str) -> Optional[GraphState]:
        """Retrieve state."""
        return await self.store.get_task(execution_id)

    async def save_checkpoint(self, state: GraphState) -> None:
        """Persist current state."""
        await self.store.save_task(state)

    async def recover_active_tasks(self) -> int:
        """Called on startup. Finds tasks that were running when the server died."""
        active = await self.store.list_active_tasks()
        count = 0
        for task in active:
            if task.status == ExecutionStatus.RUNNING:
                logger.info("Recovering orphaned task: %s", task.execution_id)
                # In a future iteration, re-queue these via a TaskQueue
                count += 1
        return count


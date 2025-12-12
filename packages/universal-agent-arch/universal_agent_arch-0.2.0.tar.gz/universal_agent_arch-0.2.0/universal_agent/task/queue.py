"""
universal_agent.task.queue

Abstraction for queuing tasks to decouple producers from workers.
"""

from __future__ import annotations

from typing import Optional

from universal_agent.contracts import ITaskQueue

class InMemoryTaskQueue(ITaskQueue):
    """Simple asyncio queue for single-process deployments."""

    def __init__(self):
        import asyncio

        self._queue = asyncio.Queue()

    async def enqueue(self, execution_id: str, priority: int = 0) -> None:
        await self._queue.put(execution_id)

    async def dequeue(self) -> Optional[str]:
        return await self._queue.get()


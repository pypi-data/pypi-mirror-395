"""
universal_agent.task.store

Persistence layer for durable task state.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import JSON, Column, DateTime, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from universal_agent.contracts import ITaskStore
from universal_agent.graph.state import GraphState

logger = logging.getLogger(__name__)

Base = declarative_base()


class TaskModel(Base):
    """SQL table definition for Tasks."""

    __tablename__ = "tasks"

    execution_id = Column(String, primary_key=True)
    graph_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    state_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc))


class SQLTaskStore(ITaskStore):
    """SQLAlchemy implementation of the Task Store."""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def init_db(self) -> None:
        """Create tables if they don't exist."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_task(self, state: GraphState) -> None:
        async with self.async_session() as session:
            async with session.begin():
                data = state.model_dump(mode="json")
                stmt = select(TaskModel).where(TaskModel.execution_id == state.execution_id)
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()
                if existing:
                    existing.status = state.status
                    existing.state_json = data
                    existing.updated_at = datetime.now(timezone.utc)
                else:
                    new_task = TaskModel(
                        execution_id=state.execution_id,
                        graph_name=state.graph_name,
                        status=state.status,
                        state_json=data,
                        created_at=state.created_at,
                    )
                    session.add(new_task)
            await session.commit()

    async def get_task(self, execution_id: str) -> Optional[GraphState]:
        async with self.async_session() as session:
            stmt = select(TaskModel).where(TaskModel.execution_id == execution_id)
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
            if not record:
                return None
            return GraphState(**record.state_json)

    async def list_active_tasks(self) -> List[GraphState]:
        async with self.async_session() as session:
            stmt = select(TaskModel).where(TaskModel.status.in_(["running", "suspended", "pending"]))
            result = await session.execute(stmt)
            records = result.scalars().all()
            return [GraphState(**r.state_json) for r in records]


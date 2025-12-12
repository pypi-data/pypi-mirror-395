"""
universal_agent.graph.state

Defines the dynamic runtime state of a graph execution.
Tracks pointer, context, and history. Serializable for durability.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Lifecycle status of a graph execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    """Outcome of a single node execution."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


class StepRecord(BaseModel):
    """Immutable record of a completed step in the graph history."""

    step_id: str = Field(default_factory=lambda: str(uuid4()))
    node_id: str
    status: StepStatus
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    start_time: datetime
    end_time: datetime

    @property
    def duration_seconds(self) -> float:
        return (self.end_time - self.start_time).total_seconds()


class SuspensionInfo(BaseModel):
    """Details about why execution is suspended (e.g., waiting for approval)."""

    reason: str
    required_input_schema: Optional[Dict[str, Any]] = None
    approval_channel: Optional[str] = None
    suspended_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GraphState(BaseModel):
    """
    Complete serializable state of a graph execution.
    Persist this to achieve durability across restarts.
    """

    execution_id: str
    graph_name: str
    graph_version: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    current_node_id: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    history: List[StepRecord] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    global_error: Optional[str] = None
    suspend_info: Optional[SuspensionInfo] = None
    last_step_output: Optional[Dict[str, Any]] = None

    def record_step(self, record: StepRecord) -> None:
        """Append a completed step to history and update metadata."""
        self.history.append(record)
        self.last_step_output = record.outputs
        self.updated_at = datetime.now(timezone.utc)

    def update_context(self, updates: Dict[str, Any]) -> None:
        """Merge new data into the global context."""
        self.context.update(updates)
        self.updated_at = datetime.now(timezone.utc)

    def transition_to(self, node_id: str) -> None:
        """Move the pointer to the next node."""
        self.current_node_id = node_id
        self.updated_at = datetime.now(timezone.utc)

    def suspend(
        self,
        reason: str,
        schema: Optional[Dict[str, Any]] = None,
        channel: Optional[str] = None,
    ) -> None:
        """Pause execution for HITL."""
        self.status = ExecutionStatus.SUSPENDED
        self.suspend_info = SuspensionInfo(
            reason=reason, required_input_schema=schema, approval_channel=channel
        )
        self.updated_at = datetime.now(timezone.utc)

    def resume(self, inputs: Optional[Dict[str, Any]] = None) -> None:
        """Clear suspension and resume execution."""
        self.status = ExecutionStatus.RUNNING
        self.suspend_info = None
        if inputs:
            self.update_context(inputs)
        self.updated_at = datetime.now(timezone.utc)

    def fail(self, error: str) -> None:
        """Mark execution as failed."""
        self.status = ExecutionStatus.FAILED
        self.global_error = error
        self.updated_at = datetime.now(timezone.utc)

    def complete(self) -> None:
        """Mark execution as completed."""
        self.status = ExecutionStatus.COMPLETED
        self.current_node_id = None
        self.updated_at = datetime.now(timezone.utc)


__all__ = [
    "ExecutionStatus",
    "StepStatus",
    "StepRecord",
    "SuspensionInfo",
    "GraphState",
]


"""
Reusable conformance tests for `ITaskStore` implementations.
Downstream adapters can import `verify_store_contract` and parametrize with their store.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from universal_agent.contracts import ITaskStore
from universal_agent.graph.state import ExecutionStatus, GraphState


async def verify_store_contract(store: ITaskStore) -> None:
    """
    Standard verification routine for any ITaskStore.

    Example usage:
        @pytest.mark.parametrize("store_impl", [MyDynamoStore(), MySQLStore()])
        @pytest.mark.asyncio
        async def test_store(store_impl):
            await verify_store_contract(store_impl)
    """
    exec_id = str(uuid.uuid4())
    state = GraphState(
        execution_id=exec_id,
        graph_name="test-graph",
        graph_version="1.0",
        context={"foo": "bar"},
        status=ExecutionStatus.PENDING,
        created_at=datetime.now(timezone.utc),
    )

    # Save
    await store.save_task(state)

    # Load
    loaded = await store.get_task(exec_id)
    assert loaded is not None
    assert loaded.execution_id == exec_id
    assert loaded.context["foo"] == "bar"
    assert loaded.status == ExecutionStatus.PENDING

    # Update
    state.status = ExecutionStatus.RUNNING
    state.context["foo"] = "baz"
    await store.save_task(state)

    reloaded = await store.get_task(exec_id)
    assert reloaded is not None
    assert reloaded.status == ExecutionStatus.RUNNING
    assert reloaded.context["foo"] == "baz"


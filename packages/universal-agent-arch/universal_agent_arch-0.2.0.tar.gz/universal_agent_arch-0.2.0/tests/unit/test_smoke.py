"""
Basic smoke tests to verify the package imports correctly.
"""

import pytest


def test_import_contracts():
    """Verify core contracts can be imported."""
    from universal_agent.contracts import ITaskStore, ITaskQueue, IToolExecutor, IRouterStrategy
    assert ITaskStore is not None
    assert ITaskQueue is not None
    assert IToolExecutor is not None
    assert IRouterStrategy is not None


def test_import_graph():
    """Verify graph module can be imported."""
    from universal_agent.graph.state import GraphState, ExecutionStatus, StepStatus
    from universal_agent.graph.model import Graph, Node, Edge
    from universal_agent.graph.engine import GraphEngine, NodeHandler
    assert GraphState is not None
    assert ExecutionStatus is not None
    assert Graph is not None
    assert GraphEngine is not None


def test_import_manifests():
    """Verify manifest schema can be imported."""
    from universal_agent.manifests.schema import (
        AgentManifest,
        GraphSpec,
        RouterSpec,
        ToolSpec,
        PolicySpec,
    )
    assert AgentManifest is not None
    assert GraphSpec is not None
    assert RouterSpec is not None
    assert ToolSpec is not None
    assert PolicySpec is not None


def test_graph_state_creation():
    """Verify GraphState can be instantiated."""
    from universal_agent.graph.state import GraphState, ExecutionStatus
    
    state = GraphState(
        execution_id="test-123",
        graph_name="test-graph",
        graph_version="1.0.0",
        context={"query": "hello"},
    )
    
    assert state.execution_id == "test-123"
    assert state.status == ExecutionStatus.PENDING
    assert state.context["query"] == "hello"


def test_graph_state_transitions():
    """Verify GraphState lifecycle methods work."""
    from universal_agent.graph.state import GraphState, ExecutionStatus
    
    state = GraphState(
        execution_id="test-456",
        graph_name="test-graph",
        graph_version="1.0.0",
    )
    
    # Test transition
    state.transition_to("node-1")
    assert state.current_node_id == "node-1"
    
    # Test suspend
    state.suspend(reason="waiting for approval")
    assert state.status == ExecutionStatus.SUSPENDED
    assert state.suspend_info is not None
    
    # Test resume
    state.resume({"approved": True})
    assert state.status == ExecutionStatus.RUNNING
    assert state.context["approved"] is True
    
    # Test complete
    state.complete()
    assert state.status == ExecutionStatus.COMPLETED


@pytest.mark.asyncio
async def test_sql_task_store():
    """Verify SQLTaskStore basic operations."""
    from universal_agent.task.store import SQLTaskStore
    from universal_agent.graph.state import GraphState, ExecutionStatus
    
    store = SQLTaskStore("sqlite+aiosqlite:///:memory:")
    await store.init_db()
    
    state = GraphState(
        execution_id="store-test-1",
        graph_name="test-graph",
        graph_version="1.0.0",
        context={"test": "data"},
    )
    
    # Save
    await store.save_task(state)
    
    # Retrieve
    loaded = await store.get_task("store-test-1")
    assert loaded is not None
    assert loaded.execution_id == "store-test-1"
    assert loaded.context["test"] == "data"
    
    # Update
    state.status = ExecutionStatus.RUNNING
    await store.save_task(state)
    
    reloaded = await store.get_task("store-test-1")
    assert reloaded.status == ExecutionStatus.RUNNING


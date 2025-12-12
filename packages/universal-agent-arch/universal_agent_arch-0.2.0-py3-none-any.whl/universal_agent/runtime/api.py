"""
universal_agent.runtime.api

REST API entrypoint for the Universal Agent runtime.
Exposes endpoints to start graphs, check status, and resume HITL flows.

Run with:
    uvicorn universal_agent.runtime.api:app --reload
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

from universal_agent.contracts import ITaskQueue, ITaskStore, IToolExecutor
from universal_agent.graph.engine import GraphEngine, NodeHandler
from universal_agent.graph.model import Graph
from universal_agent.graph.state import ExecutionStatus, GraphState
from universal_agent.manifests.loader import ManifestLoader
from universal_agent.manifests.schema import AgentManifest, GraphNodeKind, ToolProtocol
from universal_agent.runtime.config import config, load_class
from universal_agent.runtime.handlers import BaseLLMClient, HumanHandler, RouterHandler, ToolHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("universal_agent.api")

app = FastAPI(title="Universal Agent Runtime")

MANIFEST: Optional[AgentManifest] = None
GRAPHS: Dict[str, Graph] = {}
task_store: Optional[ITaskStore] = None
task_queue: Optional[ITaskQueue] = None


class RuntimeContainer:
    """Simple container for runtime singletons."""

    def __init__(
        self,
        manifest: AgentManifest,
        llm_client: BaseLLMClient,
        tool_executors: Dict[ToolProtocol, IToolExecutor],
    ) -> None:
        self.manifest = manifest
        self.llm_client = llm_client
        self.tool_executors = tool_executors


container: Optional[RuntimeContainer] = None


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event() -> None:
    """Load manifest, init task store, and compile graphs on startup."""
    global MANIFEST, container, GRAPHS, task_store, task_queue

    try:
        MANIFEST = ManifestLoader.load_from_path("manifest.yaml")
        logger.info("✅ Loaded Manifest: %s", MANIFEST.name)
    except Exception as exc:  # pragma: no cover - startup guard
        logger.error("Failed to load manifest: %s", exc)
        MANIFEST = AgentManifest(name="empty-agent", version="0.0.0")

    # Load store/queue via DI config
    store_cls = load_class(config.task_store_path, ITaskStore)
    task_store = store_cls(config.database_url)  # type: ignore[call-arg]
    if hasattr(task_store, "init_db"):
        await task_store.init_db()

    queue_cls = load_class(config.task_queue_path, ITaskQueue)
    task_queue = queue_cls()  # type: ignore[call-arg]

    llm_cls = load_class(config.llm_client_path, BaseLLMClient)
    llm_client = llm_cls()  # type: ignore[call-arg]

    local_executor_cls = load_class(config.tool_executor_local_path, IToolExecutor)
    mcp_executor_cls = load_class(config.tool_executor_mcp_path, IToolExecutor)
    tool_executors: Dict[ToolProtocol, IToolExecutor] = {
        ToolProtocol.LOCAL: local_executor_cls(),
        ToolProtocol.MCP: mcp_executor_cls(),
    }

    container = RuntimeContainer(MANIFEST, llm_client, tool_executors)

    for graph_spec in MANIFEST.graphs:
        try:
            GRAPHS[graph_spec.name] = Graph(graph_spec)
            logger.info("🔹 Compiled Graph: %s", graph_spec.name)
        except Exception as exc:  # pragma: no cover - startup guard
            logger.error("Failed to compile graph %s: %s", graph_spec.name, exc)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_handlers(state: GraphState) -> Dict[GraphNodeKind, NodeHandler]:
    if not container:
        raise HTTPException(500, "Runtime container not initialized")

    return {
        GraphNodeKind.ROUTER: RouterHandler(container.manifest, container.llm_client),
        GraphNodeKind.TOOL: ToolHandler(container.manifest, container.tool_executors),
        GraphNodeKind.HUMAN: HumanHandler(state),
    }


async def run_engine_background(engine: GraphEngine) -> None:
    await engine.run()
    logger.info("🏁 Execution %s finished with status: %s", engine.state.execution_id, engine.state.status)
    if task_store:
        await task_store.save_task(engine.state)


# ---------------------------------------------------------------------------
# API models
# ---------------------------------------------------------------------------
class ExecuteRequest(BaseModel):
    input: Dict[str, Any]


class ResumeRequest(BaseModel):
    input: Dict[str, Any]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def health_check() -> Dict[str, Any]:
    return {
        "status": "ok",
        "agent": MANIFEST.name if MANIFEST else "unknown",
        "loaded_graphs": list(GRAPHS.keys()),
    }


@app.post("/graphs/{graph_name}/executions", status_code=201)
async def start_execution(graph_name: str, request: ExecuteRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    if graph_name not in GRAPHS:
        raise HTTPException(404, f"Graph '{graph_name}' not found")

    if not task_store:
        raise HTTPException(500, "Task store not initialized")

    graph = GRAPHS[graph_name]
    exec_id = str(uuid.uuid4())
    state = GraphState(
        execution_id=exec_id,
        graph_name=graph_name,
        graph_version=graph.version,
        context=request.input,
    )
    await task_store.save_task(state)

    handlers = get_handlers(state)
    engine = GraphEngine(graph, state, handlers)
    background_tasks.add_task(run_engine_background, engine)

    return {
        "execution_id": exec_id,
        "status": ExecutionStatus.PENDING,
        "monitor_url": f"/executions/{exec_id}",
    }


@app.get("/executions/{execution_id}")
async def get_execution(execution_id: str) -> GraphState:
    if not task_store:
        raise HTTPException(500, "Task store not initialized")
    state = await task_store.get_task(execution_id)
    if not state:
        raise HTTPException(404, "Execution not found")
    return state


@app.post("/executions/{execution_id}/resume")
async def resume_execution(
    execution_id: str, request: ResumeRequest, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    if not task_store:
        raise HTTPException(500, "Task store not initialized")
    state = await task_store.get_task(execution_id)
    if not state:
        raise HTTPException(404, "Execution not found")
    if state.status != ExecutionStatus.SUSPENDED:
        raise HTTPException(400, f"Cannot resume execution in status: {state.status}")

    logger.info("Resuming execution %s with input: %s", execution_id, request.input)
    state.resume(request.input)
    await task_store.save_task(state)

    graph = GRAPHS[state.graph_name]
    handlers = get_handlers(state)
    engine = GraphEngine(graph, state, handlers)
    background_tasks.add_task(run_engine_background, engine)

    return {"status": "resumed"}


__all__ = ["app"]


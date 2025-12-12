"""
universal_agent.graph.engine

Asynchronous runtime engine driving graph execution.
Delegates node execution to injected handlers and manages state transitions.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from universal_agent.graph.model import Edge, Graph, Node
from universal_agent.graph.state import ExecutionStatus, GraphState, StepRecord, StepStatus
from universal_agent.manifests.schema import EdgeTrigger, GraphNodeKind

logger = logging.getLogger(__name__)


class NodeExecutionError(Exception):
    """Raised when a node fails to execute."""


class NodeHandler(ABC):
    """
    Interface for node execution.
    Implementations encapsulate side effects (LLM calls, tools, etc.).
    """

    @abstractmethod
    async def execute(
        self, node: Node, inputs: Dict[str, Any], context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute logic for a specific node."""
        raise NotImplementedError


class GraphEngine:
    """Main driver for graph execution."""

    def __init__(
        self,
        graph: Graph,
        state: GraphState,
        handlers: Dict[GraphNodeKind, NodeHandler],
        observer: Optional[Any] = None,
    ) -> None:
        self.graph = graph
        self.state = state
        self.handlers = handlers
        self.observer = observer

        if self.state.graph_name != self.graph.name:
            raise ValueError("State belongs to a different graph")

    async def run(self, max_steps: int = 100) -> None:
        """Run the graph until completion, suspension, failure, or step limit."""
        if self.state.status == ExecutionStatus.PENDING:
            self.state.status = ExecutionStatus.RUNNING
            self.state.transition_to(self.graph.entry_node.id)

        steps = 0
        while self.state.status == ExecutionStatus.RUNNING and steps < max_steps:
            await self.step()
            steps += 1

        if steps >= max_steps and self.state.status == ExecutionStatus.RUNNING:
            logger.warning("Graph %s hit max_steps (%s)", self.graph.name, max_steps)
            self.state.fail("Max execution steps exceeded")

    async def step(self) -> None:
        """Execute a single atomic step of the graph."""
        if not self.state.current_node_id:
            self.state.complete()
            return

        current_node_id = self.state.current_node_id
        try:
            node = self.graph.get_node(current_node_id)
        except KeyError:
            self.state.fail(f"Pointer references missing node: {current_node_id}")
            return

        logger.info("Stepping node: %s (%s)", node.id, node.kind)
        start_time = datetime.now(timezone.utc)

        inputs = self._resolve_inputs(node)

        step_status = StepStatus.SUCCESS
        outputs: Dict[str, Any] = {}
        error_msg: Optional[str] = None
        span = None

        try:
            if self.observer:
                span = self.observer.on_step_start(self.state, node.id, inputs)
            outputs = await self._execute_node(node, inputs)
            if node.spec.output_map:
                updates = self._map_outputs(node, outputs)
                if updates:
                    self.state.update_context(updates)
        except Exception as exc:
            logger.error("Error executing node %s: %s", node.id, exc, exc_info=True)
            step_status = StepStatus.ERROR
            error_msg = str(exc)

        end_time = datetime.now(timezone.utc)

        record = StepRecord(
            node_id=node.id,
            status=step_status,
            inputs=inputs,
            outputs=outputs if step_status == StepStatus.SUCCESS else None,
            error_message=error_msg,
            start_time=start_time,
            end_time=end_time,
        )
        self.state.record_step(record)
        if self.observer and span:
            self.observer.on_step_end(span, record)

        if self.state.status == ExecutionStatus.SUSPENDED:
            return

        await self._transition(node, step_status)

    async def _execute_node(self, node: Node, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch execution to the appropriate handler."""
        handler = self.handlers.get(node.kind)
        if not handler:
            raise NotImplementedError(f"No handler registered for kind: {node.kind}")
        return await handler.execute(node, inputs, self.state.context)

    async def _transition(self, node: Node, status: StepStatus) -> None:
        """Find the next node based on status and edge conditions."""
        trigger = EdgeTrigger.SUCCESS if status == StepStatus.SUCCESS else EdgeTrigger.ERROR
        edges = self.graph.get_transitions(node.id, trigger)

        if not edges:
            if status == StepStatus.ERROR:
                self.state.fail(f"Unhandled error at node {node.id}")
            else:
                self.state.complete()
            return

        selected_edge: Optional[Edge] = None
        for edge in edges:
            if self._evaluate_condition(edge):
                selected_edge = edge
                break

        if selected_edge:
            logger.info("Transition: %s -> %s", node.id, selected_edge.target.id)
            self.state.transition_to(selected_edge.target.id)
        else:
            if status == StepStatus.ERROR:
                self.state.fail("Error occurred but no error path matched conditions.")
            else:
                logger.info("Node %s finished with no matching conditions. Completing.", node.id)
                self.state.complete()

    def _evaluate_condition(self, edge: Edge) -> bool:
        """
        Check if an edge should be traversed.
        WARNING: uses eval; replace with a safe evaluator/DSL in production.
        """
        if not edge.expression:
            return True

        context = self.state.context.copy()
        context["last_output"] = self.state.last_step_output

        try:
            return bool(eval(edge.expression, {}, context))  # nosec: B307
        except Exception as exc:
            logger.error(
                "Failed to evaluate edge expression '%s': %s", edge.expression, exc
            )
            return False

    def _resolve_inputs(self, node: Node) -> Dict[str, Any]:
        """Map global context to node inputs using node.spec.inputs mapping."""
        result: Dict[str, Any] = {}
        inputs_config = node.spec.inputs or {}

        for key, value_template in inputs_config.items():
            if isinstance(value_template, str) and value_template.startswith("$"):
                path = value_template.lstrip("$")
                result[key] = self._lookup_path(self.state.context, path)
            else:
                result[key] = value_template

        return result

    def _map_outputs(self, node: Node, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Map node outputs back into global context using node.spec.output_map."""
        updates: Dict[str, Any] = {}
        for output_key, context_key in node.spec.output_map.items():
            if output_key in outputs:
                updates[context_key] = outputs[output_key]
        return updates

    def _lookup_path(self, context: Dict[str, Any], path: str) -> Any:
        """Resolve dotted paths from context (e.g., 'user.name')."""
        parts = path.split(".")
        value: Any = context
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        return value


__all__ = ["GraphEngine", "NodeHandler", "NodeExecutionError"]


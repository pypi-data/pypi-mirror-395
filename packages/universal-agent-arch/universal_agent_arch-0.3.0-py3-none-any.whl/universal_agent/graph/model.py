"""
universal_agent.graph.model

Internal runtime representations of the Graph structure.
Wraps declarative specs into queryable objects optimized for the execution engine.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from universal_agent.manifests.schema import EdgeTrigger, GraphEdgeSpec, GraphNodeSpec, GraphSpec

logger = logging.getLogger(__name__)


class GraphValidationError(Exception):
    """Raised when graph integrity checks fail (e.g., dead ends, invalid refs)."""


class Node:
    """Runtime wrapper for a graph node."""

    def __init__(self, spec: GraphNodeSpec) -> None:
        self.spec = spec
        self.id = spec.id
        self.kind = spec.kind
        # Pre-calculate downstream connections
        self.outgoing_edges: List[Edge] = []

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Node id={self.id} kind={self.kind}>"


class Edge:
    """Runtime wrapper for a graph edge."""

    def __init__(self, spec: GraphEdgeSpec, source: Node, target: Node) -> None:
        self.spec = spec
        self.source = source
        self.target = target
        self.trigger = spec.condition.trigger
        self.expression = spec.condition.expression

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Edge {self.source.id} -> {self.target.id} [{self.trigger}]>"


class Graph:
    """
    Immutable runtime graph structure.

    Responsibilities:
    - Index nodes by ID for O(1) lookup.
    - Validate structural integrity.
    - Provide traversal helpers for the execution engine.
    """

    def __init__(self, spec: GraphSpec) -> None:
        self.spec = spec
        self.name = spec.name
        self.version = spec.version

        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

        self._build_graph()
        self._validate()

    @property
    def entry_node(self) -> Node:
        """Get the starting node of the graph."""
        return self.nodes[self.spec.entry_node]

    def get_node(self, node_id: str) -> Node:
        """Retrieve a node by ID. Raises KeyError if missing."""
        return self.nodes[node_id]

    def get_transitions(
        self, node_id: str, trigger: Optional[EdgeTrigger] = None
    ) -> List[Edge]:
        """
        Get outgoing edges from a node, optionally filtered by trigger type.
        """
        node = self.nodes[node_id]
        if trigger is None:
            return node.outgoing_edges
        return [edge for edge in node.outgoing_edges if edge.trigger == trigger]

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #
    def _build_graph(self) -> None:
        """Hydrate specs into runtime objects."""
        for node_spec in self.spec.nodes:
            if node_spec.id in self.nodes:
                raise GraphValidationError(f"Duplicate node ID found: {node_spec.id}")
            self.nodes[node_spec.id] = Node(node_spec)

        for edge_spec in self.spec.edges:
            if edge_spec.from_node not in self.nodes:
                raise GraphValidationError(
                    f"Edge references missing source node: {edge_spec.from_node}"
                )
            if edge_spec.to_node not in self.nodes:
                raise GraphValidationError(
                    f"Edge references missing target node: {edge_spec.to_node}"
                )

            source = self.nodes[edge_spec.from_node]
            target = self.nodes[edge_spec.to_node]
            edge = Edge(edge_spec, source, target)
            self.edges.append(edge)
            source.outgoing_edges.append(edge)

    def _validate(self) -> None:
        """Perform structural integrity checks."""
        if self.spec.entry_node not in self.nodes:
            raise GraphValidationError(
                f"Entry node '{self.spec.entry_node}' does not exist in graph '{self.name}'"
            )

        # Detect unreachable nodes (BFS from entry)
        visited: Set[str] = set()
        queue: List[Node] = [self.entry_node]
        visited.add(self.entry_node.id)

        while queue:
            current = queue.pop(0)
            for edge in current.outgoing_edges:
                if edge.target.id not in visited:
                    visited.add(edge.target.id)
                    queue.append(edge.target)

        unreachable = set(self.nodes.keys()) - visited
        if unreachable:
            logger.warning("Graph '%s' has unreachable nodes: %s", self.name, unreachable)


__all__ = ["Graph", "Node", "Edge", "GraphValidationError"]


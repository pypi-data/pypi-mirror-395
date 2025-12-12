"""
universal_agent.manifests.validator

Performs semantic validation on the loaded AgentManifest.
Ensures that all references resolve to existing definitions.
"""

from __future__ import annotations

from typing import List

from .schema import AgentManifest, GraphNodeKind


class ManifestValidationError(Exception):
    pass


class ManifestValidator:
    def __init__(self, manifest: AgentManifest):
        self.manifest = manifest
        self.graph_ids = {g.name for g in manifest.graphs}
        self.router_ids = {r.name for r in manifest.routers}
        self.tool_ids = {t.name for t in manifest.tools}
        self.policy_ids = {p.name for p in manifest.policies}
        self.memory_ids = {m.name for m in manifest.memories}
        self.profile_ids = {c.name for c in manifest.context_profiles}

    def validate(self) -> None:
        """Run all validation checks."""
        errors: List[str] = []
        errors.extend(self._validate_graphs())
        errors.extend(self._validate_tasks())
        errors.extend(self._validate_routers())

        if errors:
            raise ManifestValidationError(
                "Manifest semantic validation failed:\n" + "\n".join(errors)
            )

    def _validate_graphs(self) -> List[str]:
        errors: List[str] = []
        for graph in self.manifest.graphs:
            for node in graph.nodes:
                if node.kind == GraphNodeKind.ROUTER:
                    if not node.router or node.router.name not in self.router_ids:
                        errors.append(
                            f"Graph '{graph.name}' node '{node.id}' references unknown router "
                            f"'{node.router.name if node.router else 'None'}'"
                        )
                elif node.kind == GraphNodeKind.TOOL:
                    if not node.tool or node.tool.name not in self.tool_ids:
                        errors.append(
                            f"Graph '{graph.name}' node '{node.id}' references unknown tool "
                            f"'{node.tool.name if node.tool else 'None'}'"
                        )
                elif node.kind == GraphNodeKind.SUBGRAPH:
                    if not node.graph or node.graph.name not in self.graph_ids:
                        errors.append(
                            f"Graph '{graph.name}' node '{node.id}' references unknown subgraph "
                            f"'{node.graph.name if node.graph else 'None'}'"
                        )

                for binding in node.memory_bindings:
                    if binding.store not in self.memory_ids:
                        errors.append(
                            f"Graph '{graph.name}' node '{node.id}' references unknown memory store "
                            f"'{binding.store}'"
                        )

            node_ids = {n.id for n in graph.nodes}
            for edge in graph.edges:
                if edge.from_node not in node_ids:
                    errors.append(
                        f"Graph '{graph.name}' edge references unknown source node '{edge.from_node}'"
                    )
                if edge.to_node not in node_ids:
                    errors.append(
                        f"Graph '{graph.name}' edge references unknown target node '{edge.to_node}'"
                    )

        return errors

    def _validate_tasks(self) -> List[str]:
        errors: List[str] = []
        for task in self.manifest.tasks:
            if task.graph.name not in self.graph_ids:
                errors.append(
                    f"Task '{task.name}' references unknown graph '{task.graph.name}'"
                )
        return errors

    def _validate_routers(self) -> List[str]:
        errors: List[str] = []
        for router in self.manifest.routers:
            if router.policy and router.policy not in self.policy_ids:
                errors.append(
                    f"Router '{router.name}' references unknown policy '{router.policy}'"
                )
        return errors


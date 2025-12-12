"""
universal_agent.router.selector

Logic for selecting the appropriate model or tool based on RouterSpecs.
"""

from __future__ import annotations

from typing import Any, Dict, List

from universal_agent.manifests.schema import RouterSpec, ToolSelectionRule


class SelectionResult:
    def __init__(self, model: str | None, allowed_tools: List[str]):
        self.model = model
        self.allowed_tools = allowed_tools


class RouterSelector:
    def __init__(self, spec: RouterSpec):
        self.spec = spec

    def select(self, context: Dict[str, Any]) -> SelectionResult:
        """Determine the model and available tools for the current step."""
        model = self.spec.default_model
        allowed_tools = set()

        for rule in self.spec.tool_selection_rules:
            if self._evaluate_rule(rule, context):
                allowed_tools.update(rule.tools)

        return SelectionResult(model=model, allowed_tools=list(allowed_tools))

    def _evaluate_rule(self, rule: ToolSelectionRule, context: Dict[str, Any]) -> bool:
        if not rule.conditions:
            return True
        for key, value in rule.conditions.items():
            if context.get(key) != value:
                return False
        return True


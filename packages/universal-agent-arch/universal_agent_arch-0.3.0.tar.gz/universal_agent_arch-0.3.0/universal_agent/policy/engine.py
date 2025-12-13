"""
universal_agent.policy.engine

Evaluates actions against the policies defined in the manifest.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from universal_agent.manifests.schema import PolicyAction, PolicyRule, PolicySpec

logger = logging.getLogger(__name__)


class PolicyEngine:
    def __init__(self, policies: List[PolicySpec]):
        self.policies = {p.name: p for p in policies}

    def check(self, policy_name: str, target: str, context: Dict[str, Any] | None = None) -> PolicyAction:
        """
        Check if an action on a target is allowed by the named policy.

        Args:
            policy_name: Name of the policy spec to check.
            target: The resource string (e.g., 'tool:delete_db', 'model:gpt-4').
            context: Additional context for rule evaluation.

        Returns:
            PolicyAction (ALLOW, DENY, REQUIRE_APPROVAL)
        """
        policy = self.policies.get(policy_name)
        if not policy:
            return PolicyAction.ALLOW

        for rule in policy.rules:
            if self._matches_target(rule, target) and self._matches_conditions(rule, context):
                logger.info(
                    "Policy '%s' rule '%s' matched target '%s': %s",
                    policy_name,
                    rule.description,
                    target,
                    rule.action,
                )
                return rule.action

        return PolicyAction.ALLOW

    def _matches_target(self, rule: PolicyRule, target: str) -> bool:
        """Check if the rule applies to the given target string."""
        if "*" in rule.target:
            return True
        return target in rule.target

    def _matches_conditions(self, rule: PolicyRule, context: Dict[str, Any] | None) -> bool:
        """Evaluate simple key/value conditions."""
        if not rule.conditions:
            return True
        if not context:
            return False

        for key, value in rule.conditions.items():
            if context.get(key) != value:
                return False
        return True


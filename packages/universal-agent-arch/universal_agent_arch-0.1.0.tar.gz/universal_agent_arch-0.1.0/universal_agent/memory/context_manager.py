"""
universal_agent.memory.context_manager

Builds LLM prompt context within token budgets by assembling system prompt,
tools, memories (placeholder), and pruned history from graph state.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Protocol

from pydantic import BaseModel, Field

from universal_agent.graph.state import GraphState, StepStatus
from universal_agent.manifests.schema import AgentManifest, ContextBudget, ToolSpec

logger = logging.getLogger(__name__)


class PromptContext(BaseModel):
    """
    Final prompt payload produced by ContextManager.
    """

    system_message: str
    messages: List[Dict[str, str]]  # history + user input
    tools: Optional[List[Dict[str, Any]]] = None
    token_usage: Dict[str, int] = Field(default_factory=dict)


class Tokenizer(Protocol):
    """Interface for token counting."""

    def count(self, text: str) -> int: ...


class SimpleTokenizer:
    """Fallback tokenizer using character approximation (1 token ~= 4 chars)."""

    def count(self, text: str) -> int:
        if not text:
            return 0
        return len(text) // 4


class ContextManager:
    """Orchestrates assembly of prompt context within budgets."""

    def __init__(self, manifest: AgentManifest, tokenizer: Optional[Tokenizer] = None) -> None:
        self.manifest = manifest
        self.tokenizer = tokenizer or SimpleTokenizer()
        self._profiles = {p.name: p for p in manifest.context_profiles}
        self._default_budget = ContextBudget(
            max_total_tokens=8192,
            max_history_tokens=4000,
            max_memory_tokens=1000,
            max_tool_tokens=1000,
            max_system_tokens=500,
        )

    def compose(
        self,
        state: GraphState,
        system_template: str,
        node_inputs: Dict[str, Any],
        tools: List[ToolSpec],
        profile_name: Optional[str] = None,
    ) -> PromptContext:
        """Build the final prompt context respecting token budgets."""
        profile = self._profiles.get(profile_name) if profile_name else None
        budget = profile.budget if profile else self._default_budget

        usage: Dict[str, int] = {}

        # System message
        try:
            system_msg = system_template.format(**node_inputs)
        except KeyError:
            system_msg = system_template

        sys_tokens = self.tokenizer.count(system_msg)
        if sys_tokens > budget.max_system_tokens:
            logger.warning(
                "System message exceeds budget (%s > %s). Truncating.",
                sys_tokens,
                budget.max_system_tokens,
            )
            allowed_chars = budget.max_system_tokens * 4
            system_msg = system_msg[:allowed_chars] + "..."
            sys_tokens = self.tokenizer.count(system_msg)
        usage["system"] = sys_tokens

        # Tools
        tool_definitions = [self._format_tool(t) for t in tools]
        tool_text = str(tool_definitions)
        tool_tokens = self.tokenizer.count(tool_text)
        if tool_tokens > budget.max_tool_tokens:
            logger.warning("Tools exceed budget (%s > %s)", tool_tokens, budget.max_tool_tokens)
        usage["tools"] = tool_tokens

        # Memories placeholder
        memory_tokens = 0
        usage["memory"] = memory_tokens

        # History budget
        remaining_tokens = budget.max_total_tokens - (sys_tokens + tool_tokens + memory_tokens)
        history_budget = min(remaining_tokens, budget.max_history_tokens)
        history_messages = self._build_history(state, history_budget)
        usage["history"] = sum(self.tokenizer.count(m["content"]) for m in history_messages)

        final_messages = history_messages.copy()
        if "query" in node_inputs:
            final_messages.append({"role": "user", "content": str(node_inputs["query"])})

        return PromptContext(
            system_message=system_msg,
            messages=final_messages,
            tools=tool_definitions if tool_definitions else None,
            token_usage=usage,
        )

    def _build_history(self, state: GraphState, token_budget: int) -> List[Dict[str, str]]:
        """Convert StepRecords into LLM messages, applying rolling window strategy."""
        full_history: List[Dict[str, str]] = []
        for step in state.history:
            if step.status == StepStatus.SKIPPED:
                continue

            msg_content = f"Node {step.node_id}: {step.status}\nInputs: {step.inputs}"
            if step.outputs:
                msg_content += f"\nOutputs: {step.outputs}"
            if step.error_message:
                msg_content += f"\nError: {step.error_message}"
            full_history.append({"role": "user", "content": msg_content})

        pruned_history: List[Dict[str, str]] = []
        current_tokens = 0

        if full_history:
            first = full_history[0]
            t_first = self.tokenizer.count(first["content"])
            if t_first < token_budget:
                pruned_history.append(first)
                current_tokens += t_first

        buffer: List[Dict[str, str]] = []
        for msg in reversed(full_history[1:]):
            t = self.tokenizer.count(msg["content"])
            if current_tokens + t > token_budget:
                break
            buffer.append(msg)
            current_tokens += t

        pruned_history.extend(reversed(buffer))
        return pruned_history

    def _format_tool(self, tool: ToolSpec) -> Dict[str, Any]:
        """Convert ToolSpec to an OpenAI-like function definition."""
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.config.get("input_schema", {"type": "object"}),
            },
        }


__all__ = [
    "ContextManager",
    "PromptContext",
    "Tokenizer",
    "SimpleTokenizer",
]


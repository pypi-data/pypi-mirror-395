"""
universal_agent.runtime.handlers

Concrete implementations of NodeHandlers.
These classes perform side effects:
- Calling LLMs (RouterHandler)
- Executing Tools (ToolHandler)
- Pausing for Users (HumanHandler)
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from universal_agent.contracts import IToolExecutor
from universal_agent.graph.engine import Node, NodeHandler
from universal_agent.graph.state import GraphState
from universal_agent.manifests.schema import AgentManifest, ToolProtocol

logger = logging.getLogger(__name__)


# --- Abstractions for External Dependencies ---
class BaseLLMClient(ABC):
    """Interface for LLM providers (OpenAI, Anthropic, etc.)."""

    @abstractmethod
    async def chat(
        self, model: str, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None
    ) -> Any:
        ...


# --- Handler Implementations ---
class RouterHandler(NodeHandler):
    """
    Handles ROUTER nodes.
    - Fetch RouterSpec from manifest.
    - Hydrate system prompt.
    - Build simple message list (placeholder for richer context strategy).
    - Call LLM client.
    """

    def __init__(self, manifest: AgentManifest, llm_client: BaseLLMClient):
        self.manifest = manifest
        self.llm_client = llm_client
        self._routers = {router.name: router for router in manifest.routers}

    async def execute(self, node: Node, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        router_ref = node.spec.router
        if not router_ref:
            raise ValueError(f"Router node {node.id} missing 'router' reference.")

        spec = self._routers.get(router_ref.name)
        if not spec:
            raise ValueError(f"Router '{router_ref.name}' not found in manifest.")

        # Hydrate system prompt with inputs
        try:
            system_msg = spec.system_message.format(**inputs)
        except KeyError as exc:
            logger.warning("Missing variable for system prompt: %s", exc)
            system_msg = spec.system_message

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_msg}]
        if "query" in inputs:
            messages.append({"role": "user", "content": str(inputs["query"])})

        model = spec.default_model or "gpt-4o"
        logger.info("Router %s invoking %s...", spec.name, model)
        response = await self.llm_client.chat(model, messages)

        return {
            "content": response.get("content") if isinstance(response, dict) else response,
            "tool_calls": response.get("tool_calls", []) if isinstance(response, dict) else [],
            "raw": response,
        }


class ToolHandler(NodeHandler):
    """
    Handles TOOL nodes.
    - Fetch ToolSpec from manifest.
    - Select executor based on protocol.
    - Delegate execution.
    """

    def __init__(self, manifest: AgentManifest, executors: Dict[ToolProtocol, IToolExecutor]):
        self.manifest = manifest
        self.executors = executors
        self._tools = {tool.name: tool for tool in manifest.tools}

    async def execute(self, node: Node, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        tool_ref = node.spec.tool
        if not tool_ref:
            raise ValueError(f"Tool node {node.id} missing 'tool' reference.")

        spec = self._tools.get(tool_ref.name)
        if not spec:
            raise ValueError(f"Tool '{tool_ref.name}' not found in manifest.")

        executor = self.executors.get(spec.protocol)
        if not executor:
            raise NotImplementedError(f"No executor for protocol: {spec.protocol}")

        logger.info("Executing tool %s via %s", spec.name, spec.protocol)
        try:
            result = await executor.execute(spec.config, inputs)
            return {"status": "success", "data": result}
        except Exception as exc:
            logger.error("Tool execution failed: %s", exc, exc_info=True)
            return {"status": "error", "error": str(exc)}


class HumanHandler(NodeHandler):
    """
    Handles HUMAN nodes.
    - Suspends graph state for HITL.
    """

    def __init__(self, state: GraphState):
        self.state = state

    async def execute(self, node: Node, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = inputs.get("prompt", node.spec.human_prompt or "Approval required")
        required_schema = {"approved": "boolean", "feedback": "string"}

        logger.info("Suspending graph for Human Input: %s", prompt)
        self.state.suspend(reason=prompt, schema=required_schema, channel="default")

        return {"action": "suspended", "prompt": prompt}


__all__ = [
    "BaseLLMClient",
    "IToolExecutor",
    "RouterHandler",
    "ToolHandler",
    "HumanHandler",
]


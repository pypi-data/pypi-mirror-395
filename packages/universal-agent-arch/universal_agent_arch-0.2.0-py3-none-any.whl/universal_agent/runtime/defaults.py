"""
Default stub implementations used for local development and tests.
These are referenced by the DI configuration when no overrides are provided.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from universal_agent.contracts import IToolExecutor
from universal_agent.runtime.handlers import BaseLLMClient

logger = logging.getLogger(__name__)


class MockLLMClient(BaseLLMClient):
    """Minimal LLM client that echoes content or emits a calculator tool call."""

    async def chat(
        self, model: str, messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None
    ) -> Any:
        last_msg = messages[-1]["content"].lower() if messages else ""
        if "calculate" in last_msg or "calc" in last_msg:
            return {
                "content": None,
                "tool_calls": [
                    {
                        "function": {"name": "calculator", "arguments": '{"expression": "2 + 2"}'},
                        "type": "function",
                    }
                ],
            }
        return {"content": f"[mock-{model}] {last_msg}", "tool_calls": []}


class MockToolExecutor(IToolExecutor):
    """Dummy executor that returns the arguments for inspection."""

    async def execute(self, config: Dict[str, Any], arguments: Dict[str, Any]) -> Any:
        logger.info("MockToolExecutor executing with config=%s arguments=%s", config, arguments)
        return {"echo": arguments, "config": config, "status": "mock_success"}


__all__ = ["MockLLMClient", "MockToolExecutor"]


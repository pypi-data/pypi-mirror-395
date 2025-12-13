"""
universal_agent.graph.signals

Exceptions used to control the flow of the Graph Engine.
"""

from typing import Any, Dict, Optional


class InterruptSignal(Exception):
    """
    Raised by a NodeHandler (e.g., HumanHandler, PolicyEngine) to
    immediately pause graph execution and save state.
    """

    def __init__(
        self,
        reason: str,
        input_schema: Optional[Dict[str, Any]] = None,
        approval_channel: Optional[str] = None,
    ):
        self.reason = reason
        self.input_schema = input_schema
        self.approval_channel = approval_channel
        super().__init__(reason)


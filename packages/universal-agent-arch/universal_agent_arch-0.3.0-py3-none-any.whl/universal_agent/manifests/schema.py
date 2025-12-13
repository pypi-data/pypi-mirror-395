"""
universal_agent.manifests.schema

Pydantic models defining the declarative manifest format for the Universal Agent Architecture.

This schema describes:

- Graphs (nodes, edges, transitions, retry/timeout)
- Tasks (durable work units bound to graphs)
- Tools (capabilities, protocols, sandbox profiles)
- Memory stores (vector/KV/doc)
- Routers (model/tool selection, context profiles)
- Policies (allow/deny/require-approval rules)
- Sandboxes (execution environments)
- Context profiles (token budgets and summarization)
- Observer config (sinks for metrics/logs/traces)
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, conint

# ---------------------------------------------------------------------------
# Core enums
# ---------------------------------------------------------------------------


class GraphNodeKind(str, Enum):
    TASK = "task"
    ROUTER = "router"
    TOOL = "tool"
    SUBGRAPH = "subgraph"
    HUMAN = "human"  # explicit human-in-the-loop node


class EdgeTrigger(str, Enum):
    """What causes an edge to fire."""

    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    APPROVAL = "approval"
    REJECTION = "rejection"
    CUSTOM = "custom"  # e.g. named events


class RetryStrategy(str, Enum):
    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"


class ToolProtocol(str, Enum):
    MCP = "mcp"
    HTTP = "http"
    SUBPROCESS = "subprocess"
    LOCAL = "local"


class MemoryStoreKind(str, Enum):
    VECTOR = "vector"
    KV = "kv"
    DOC = "doc"


class RouterStrategyKind(str, Enum):
    RULE = "rule"
    LLM = "llm"
    HYBRID = "hybrid"


class PolicyAction(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"


class ObserverSinkKind(str, Enum):
    STDOUT = "stdout"
    OTEL = "otel"
    PROMETHEUS = "prometheus"
    FILE = "file"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Common small models
# ---------------------------------------------------------------------------


class RetryPolicy(BaseModel):
    """Retry configuration for steps/tasks."""

    strategy: RetryStrategy = Field(
        default=RetryStrategy.FIXED,
        description="Retry strategy to use.",
    )
    max_attempts: conint(ge=0) = Field(
        default=3,
        description="Maximum number of attempts including the initial one.",
    )
    backoff_seconds: float = Field(
        default=1.0,
        description="Base backoff in seconds for FIXED/EXPONENTIAL strategies.",
    )
    max_backoff_seconds: Optional[float] = Field(
        default=None,
        description="Upper bound on backoff delay, if any.",
    )


class TimeoutPolicy(BaseModel):
    """Timeout configuration for a node or graph."""

    seconds: float = Field(..., description="Maximum allowed runtime in seconds.")
    cancel_on_timeout: bool = Field(
        default=True,
        description="If true, the step/task is cancelled on timeout.",
    )


class Metadata(BaseModel):
    """Arbitrary metadata for extension/annotations."""

    tags: List[str] = Field(default_factory=list)
    extra: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Context management
# ---------------------------------------------------------------------------


class ContextBudget(BaseModel):
    """Token budgets for building prompts."""

    max_total_tokens: int = Field(
        ...,
        description="Hard limit for total tokens in the composed prompt.",
    )
    max_history_tokens: int = Field(
        default=1024,
        description="Maximum tokens allocated to conversation/task history.",
    )
    max_memory_tokens: int = Field(
        default=2048,
        description="Maximum tokens allocated to retrieved memories.",
    )
    max_tool_tokens: int = Field(
        default=1024,
        description="Maximum tokens allocated to tool descriptions/manifests.",
    )
    max_system_tokens: int = Field(
        default=512,
        description="Maximum tokens reserved for system instructions.",
    )


class ContextProfile(BaseModel):
    """Named strategy for composing context for a router/model."""

    name: str = Field(..., description="Unique identifier for this profile.")
    description: Optional[str] = Field(default=None)
    budget: ContextBudget = Field(
        ..., description="Token budget associated with this profile."
    )
    summarization_model: Optional[str] = Field(
        default=None,
        description="Model identifier to use for summarization, if any.",
    )
    summarization_prompt_template: Optional[str] = Field(
        default=None,
        description=(
            "Prompt template for summarization/rolling summary. "
            "May use placeholders like {history}, {new_message}."
        ),
    )
    metadata: Metadata = Field(
        default_factory=Metadata,
        description="Optional tags and extra config.",
    )


# ---------------------------------------------------------------------------
# HITL / human approval models
# ---------------------------------------------------------------------------


class HumanApprovalChannel(BaseModel):
    """Where to surface approval requests (Slack, email, UI, etc.)."""

    name: str = Field(..., description="Logical channel name.")
    kind: str = Field(
        ...,
        description="Channel type (e.g. 'slack', 'email', 'webhook', 'console').",
    )
    target: Optional[str] = Field(
        default=None,
        description="Channel-specific target (e.g. Slack webhook URL, email address).",
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary channel-specific config.",
    )


class HumanInLoopConfig(BaseModel):
    """
    Configuration describing how a task/graph interacts with humans.
    Allows pause/approval flows and optional deadlines.
    """

    enabled: bool = Field(
        default=True,
        description="Whether HITL is enabled for this task/graph.",
    )
    approval_channel: Optional[str] = Field(
        default=None,
        description="Name of a HumanApprovalChannel to use for approval requests.",
    )
    auto_timeout_seconds: Optional[float] = Field(
        default=None,
        description="If set, auto-resolve HITL after this many seconds.",
    )
    default_on_timeout: Optional[PolicyAction] = Field(
        default=None,
        description="Default policy action when approval times out.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Graph spec
# ---------------------------------------------------------------------------


class GraphNodeRef(BaseModel):
    """Reference to a node by ID."""

    id: str


class GraphRef(BaseModel):
    """Reference to a graph by name/version."""

    name: str
    version: Optional[str] = Field(
        default=None,
        description="Optional graph version. If omitted, use latest.",
    )


class RouterRef(BaseModel):
    """Reference to a router by name."""

    name: str


class ToolRef(BaseModel):
    """Reference to a tool by name."""

    name: str


class MemoryBinding(BaseModel):
    """
    Binds a named memory store into the graph/task context.
    Example:
        - bind 'code_index' vector store for a repo assistant graph.
    """

    store: str = Field(..., description="Name of the memory store spec.")
    alias: Optional[str] = Field(
        default=None,
        description="Optional alias used within prompts/tools. Defaults to store name.",
    )
    purpose: Optional[str] = Field(
        default=None,
        description="Freeform description of how this binding is used.",
    )


class GraphNodeSpec(BaseModel):
    """A node in the logical graph."""

    id: str = Field(..., description="Unique node identifier within the graph.")
    kind: GraphNodeKind = Field(
        ...,
        description="Kind of node (task/router/tool/subgraph/human).",
    )
    label: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    # Behavior-specific fields (some only apply to certain kinds)
    graph: Optional[GraphRef] = Field(
        default=None,
        description="For SUBGRAPH nodes: which graph to call.",
    )
    router: Optional[RouterRef] = Field(
        default=None,
        description="For ROUTER nodes: which router to use.",
    )
    tool: Optional[ToolRef] = Field(
        default=None,
        description="For TOOL nodes: which tool to invoke.",
    )
    human_prompt: Optional[str] = Field(
        default=None,
        description="For HUMAN nodes: explanation/instructions shown to human.",
    )
    timeout: Optional[TimeoutPolicy] = Field(
        default=None,
        description="Optional node-specific timeout.",
    )
    retry: Optional[RetryPolicy] = Field(
        default=None,
        description="Optional node-specific retry policy.",
    )
    memory_bindings: List[MemoryBinding] = Field(
        default_factory=list,
        description="Memory stores bound into this node's context.",
    )
    context_profile: Optional[str] = Field(
        default=None,
        description="Name of ContextProfile to use at this node.",
    )
    inputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Static inputs or templates mapping state to node arguments.",
    )
    output_map: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of node result keys back into graph state keys.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


class EdgeCondition(BaseModel):
    """
    Additional constraints that must be satisfied for the edge to fire.
    Framework-specific expressions (e.g. 'result.status == "ok"')
    are allowed and interpreted by adapters.
    """

    trigger: EdgeTrigger = Field(
        default=EdgeTrigger.SUCCESS,
        description="Primary trigger for this transition.",
    )
    expression: Optional[str] = Field(
        default=None,
        description="Optional boolean expression evaluated in node context.",
    )
    event_name: Optional[str] = Field(
        default=None,
        description="Optional named event for CUSTOM triggers.",
    )


class GraphEdgeSpec(BaseModel):
    """Directed edge from one node to another with conditions."""

    from_node: str = Field(..., description="Source node ID.")
    to_node: str = Field(..., description="Target node ID.")
    condition: EdgeCondition = Field(
        default_factory=EdgeCondition,
        description="When this edge should fire.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


class GraphSpec(BaseModel):
    """
    Logical graph definition independent of any specific runtime.
    Adapters compile this to LangGraph, Step Functions, Temporal, MCP Tasks, etc.
    """

    name: str = Field(..., description="Unique graph name.")
    version: str = Field(
        default="0.1.0",
        description="Graph version string (semver recommended).",
    )
    description: Optional[str] = Field(default=None)
    entry_node: str = Field(
        ...,
        description="ID of the node where execution begins.",
    )
    nodes: List[GraphNodeSpec] = Field(
        default_factory=list, description="Graph nodes."
    )
    edges: List[GraphEdgeSpec] = Field(
        default_factory=list, description="Graph edges."
    )
    state_schema: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSONSchema describing the shared graph state/context shape.",
    )
    timeout: Optional[TimeoutPolicy] = Field(
        default=None,
        description="Optional graph-level timeout.",
    )
    retry: Optional[RetryPolicy] = Field(
        default=None,
        description="Optional graph-level retry policy.",
    )
    hitl: Optional[HumanInLoopConfig] = Field(
        default=None,
        description="Optional human-in-the-loop configuration for this graph.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Task templates
# ---------------------------------------------------------------------------


class TaskTemplate(BaseModel):
    """
    Declarative template for spawning tasks.
    Tasks are durable instances that execute a graph with given input/output schemas.
    """

    name: str = Field(..., description="Unique task template name.")
    description: Optional[str] = Field(default=None)
    graph: GraphRef = Field(..., description="Which graph this template executes.")
    input_schema: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "JSONSchema-like dict describing expected input payload shape."
        ),
    )
    output_schema: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "JSONSchema-like dict describing expected output payload shape."
        ),
    )
    default_sandbox: Optional[str] = Field(
        default=None,
        description="Name of sandbox profile to use by default, if any.",
    )
    default_context_profile: Optional[str] = Field(
        default=None,
        description="Name of context profile to use by default.",
    )
    hitl: Optional[HumanInLoopConfig] = Field(
        default=None,
        description="Optional HITL configuration overriding graph-level settings.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Tools and sandboxes
# ---------------------------------------------------------------------------


class SandboxProfile(BaseModel):
    """
    Execution environment profile for running tools or code.
    Does not define *how* to implement isolation, only capabilities.
    """

    name: str = Field(..., description="Sandbox profile name.")
    description: Optional[str] = Field(default=None)
    net: bool = Field(
        default=False,
        description="Whether network access is permitted.",
    )
    fs_mode: str = Field(
        default="none",
        description="Filesystem mode: 'none', 'read-only', 'read-write', or custom.",
    )
    max_runtime_seconds: float = Field(
        default=30.0,
        description="Maximum allowed runtime for a single command.",
    )
    max_memory_mb: int = Field(
        default=512,
        description="Maximum memory allowed (approximate).",
    )
    cpu_cores: float = Field(
        default=1.0,
        description="Approximate number of CPU cores assigned.",
    )
    gpu: bool = Field(
        default=False,
        description="Whether GPU access is allowed/required.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


class ToolPolicyRef(BaseModel):
    """Reference to a policy by name."""

    name: str


class ToolSpec(BaseModel):
    """
    Declarative definition of a tool.
    Tools are capabilities (MCP, HTTP, subprocess, local) available to graphs.
    """

    name: str = Field(..., description="Unique tool name.")
    description: Optional[str] = Field(default=None)
    protocol: ToolProtocol = Field(
        ..., description="Underlying protocol/transport for this tool."
    )
    tags: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Protocol-specific configuration (e.g., MCP server address, "
            "HTTP URL, CLI command)."
        ),
    )
    sandbox_profile: Optional[str] = Field(
        default=None,
        description="Name of sandbox profile required/preferred by this tool.",
    )
    policy: Optional[ToolPolicyRef] = Field(
        default=None,
        description="Optional reference to a policy controlling this tool.",
    )
    secrets: List[str] = Field(
        default_factory=list,
        description="Environment variable names this tool requires access to.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Memory stores
# ---------------------------------------------------------------------------


class MemoryStoreSpec(BaseModel):
    """
    Declarative memory store definition (vector, KV, document, etc.).
    """

    name: str = Field(..., description="Unique memory store name.")
    kind: MemoryStoreKind = Field(
        ..., description="Type of memory store (vector/kv/doc)."
    )
    backend: str = Field(
        ...,
        description=(
            "Backend implementation identifier (e.g. 'qdrant', 'chroma', "
            "'redis', 'file', 'custom')."
        ),
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Backend-specific configuration options.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Router & policy
# ---------------------------------------------------------------------------


class ToolSelectionRule(BaseModel):
    """
    Rule for selecting tools given context.
    Adapters interpret 'conditions' using their own expression language.
    """

    description: Optional[str] = Field(default=None)
    tools: List[str] = Field(
        default_factory=list,
        description="Tool names that this rule enables/preferences.",
    )
    conditions: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Arbitrary condition structure (e.g., match on task name, "
            "user role, graph node, etc.)."
        ),
    )


class RouterSpec(BaseModel):
    """
    Declarative router configuration.
    Controls model selection, tool selection, and optional policy hooks.
    """

    name: str = Field(..., description="Router name.")
    description: Optional[str] = Field(default=None)
    strategy: RouterStrategyKind = Field(
        ..., description="Routing strategy (rule/llm/hybrid)."
    )
    model_candidates: List[str] = Field(
        default_factory=list,
        description="Set of models this router may choose from.",
    )
    default_model: Optional[str] = Field(
        default=None,
        description="Default model if no rule/LLM overrides it.",
    )
    tool_selection_rules: List[ToolSelectionRule] = Field(
        default_factory=list,
        description="Rules that influence which tools are available/selected.",
    )
    policy: Optional[str] = Field(
        default=None,
        description="Name of a PolicySpec controlling this router.",
    )
    context_profile: Optional[str] = Field(
        default=None,
        description="Name of ContextProfile to use by default.",
    )
    system_message: str = Field(
        default="You are a helpful assistant.",
        description="System prompt template; may reference state via {templates}.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


class PolicyRule(BaseModel):
    """
    Single policy rule.
    'target' strings can use simple conventions, e.g.:
        - 'tool:delete_db'
        - 'model:qwen2.5-32b'
        - 'graph:devops_incident'
        - 'task:prod_maintenance'
    """

    id: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    target: List[str] = Field(
        default_factory=list,
        description="List of target selectors this rule applies to.",
    )
    conditions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conditions under which this rule applies.",
    )
    action: PolicyAction = Field(..., description="Outcome when this rule matches.")
    approval_channel: Optional[str] = Field(
        default=None,
        description=(
            "Name of HumanApprovalChannel to use when action=REQUIRE_APPROVAL."
        ),
    )
    metadata: Metadata = Field(default_factory=Metadata)


class PolicySpec(BaseModel):
    """
    Collection of policy rules under a single logical name.
    """

    name: str = Field(..., description="Policy name.")
    description: Optional[str] = Field(default=None)
    rules: List[PolicyRule] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Observer config
# ---------------------------------------------------------------------------


class ObserverSinkSpec(BaseModel):
    """
    Configuration for an observer sink.
    Examples:
        - stdout logger
        - OTEL exporter
        - Prometheus metrics endpoint
    """

    name: str = Field(..., description="Sink name.")
    kind: ObserverSinkKind = Field(
        ..., description="Sink type (stdout/otel/prometheus/file/custom)."
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Sink-specific configuration.",
    )
    metadata: Metadata = Field(default_factory=Metadata)


class ObserverConfig(BaseModel):
    """
    High-level configuration for the observer/telemetry system.
    """

    sinks: List[ObserverSinkSpec] = Field(default_factory=list)
    default_tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Tags added to all telemetry records (e.g. environment).",
    )
    metadata: Metadata = Field(default_factory=Metadata)


# ---------------------------------------------------------------------------
# Top-level manifest
# ---------------------------------------------------------------------------


class AgentManifest(BaseModel):
    """
    Top-level manifest describing a Universal Agent system.
    This is the primary file parsed by the runtime.
    """

    name: str = Field(..., description="Manifest name.")
    version: str = Field(
        default="0.1.0",
        description="Manifest version (semver recommended).",
    )
    description: Optional[str] = Field(default=None)
    graphs: List[GraphSpec] = Field(default_factory=list)
    tasks: List[TaskTemplate] = Field(default_factory=list)
    tools: List[ToolSpec] = Field(default_factory=list)
    memories: List[MemoryStoreSpec] = Field(default_factory=list)
    routers: List[RouterSpec] = Field(default_factory=list)
    policies: List[PolicySpec] = Field(default_factory=list)
    sandboxes: List[SandboxProfile] = Field(default_factory=list)
    context_profiles: List[ContextProfile] = Field(default_factory=list)
    approval_channels: List[HumanApprovalChannel] = Field(
        default_factory=list,
        description="Named channels for human approvals.",
    )
    observer: Optional[ObserverConfig] = Field(default=None)
    metadata: Metadata = Field(default_factory=Metadata)
    source_url: Optional[HttpUrl] = Field(
        default=None,
        description="Optional URL where this manifest is hosted (for discovery).",
    )


__all__ = [
    # enums
    "GraphNodeKind",
    "EdgeTrigger",
    "RetryStrategy",
    "ToolProtocol",
    "MemoryStoreKind",
    "RouterStrategyKind",
    "PolicyAction",
    "ObserverSinkKind",
    # core models
    "RetryPolicy",
    "TimeoutPolicy",
    "Metadata",
    "ContextBudget",
    "ContextProfile",
    "HumanApprovalChannel",
    "HumanInLoopConfig",
    "GraphNodeRef",
    "GraphRef",
    "RouterRef",
    "ToolRef",
    "MemoryBinding",
    "GraphNodeSpec",
    "EdgeCondition",
    "GraphEdgeSpec",
    "GraphSpec",
    "TaskTemplate",
    "SandboxProfile",
    "ToolPolicyRef",
    "ToolSpec",
    "MemoryStoreSpec",
    "ToolSelectionRule",
    "RouterSpec",
    "PolicyRule",
    "PolicySpec",
    "ObserverSinkSpec",
    "ObserverConfig",
    "AgentManifest",
]


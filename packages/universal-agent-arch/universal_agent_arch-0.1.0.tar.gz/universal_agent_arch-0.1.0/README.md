## Universal Agent Architecture (UAA)

The Kernel → Fabric → Nexus trinity for production-grade AI agents. UAA is not another prompt loop — it is the operating system that makes LLM-powered systems durable, observable, and pluggable by applying mature distributed-systems patterns to non-deterministic functions.

### Why This Feels “Already Written” (Convergent Evolution)
Senior distributed systems engineers eventually rediscover the same five primitives when building reliable agent platforms. UAA names them, wires them, and ships a reference implementation.

| Your abstraction | What it really is | Distributed-systems analog | Who implemented it in the wild |
| --- | --- | --- | --- |
| Graph (OS) | State machine definition | Kubernetes Operators / Temporal Workflows | LangGraph, AWS Step Functions, Azure Logic Apps |
| Task (Process) | Durable work unit with checkpointing | Celery Jobs / Kubernetes Jobs / systemd units | LangGraph checkpoints, AWS DevOps Agent, Temporal Activities |
| Router (Brain) | Pattern matching + LLM selection | Load balancer / API gateway routing rules | MCP / Auto-routing across LLMs, OpenAI function router |
| Tools (Hands) | Standardized capability interface | gRPC services / REST APIs / Unix tools | MCP (Anthropic), OpenAI function calling |
| Observer (Eyes) | Distributed tracing and metrics | OpenTelemetry / Prometheus / Jaeger | LangSmith, Datadog APM, AWS X-Ray |

You did not copy this. You re-derived the canonical model by applying first principles of reliability, durability, and observability to LLMs.

### The Trinity: Kernel → Fabric → Nexus
- **Kernel (Durability, State, Execution)** — `universal_agent/`: state machines, routing, tasks, tools, tracing.
- **Fabric (Definition, Composition, Policy)** — `manifests/` + `policy/`: declarative ontologies, roles, and governance.
- **Nexus (Adapters, Protocols, Economy)** — `adapters/`: compilation targets and protocol bridges (LangGraph, Step Functions, MCP, AWS).

This separation mirrors how cloud systems are built: definitions live apart from execution, capabilities are pluggable, and observability is first-class.

### Repository Map (Proof of Structure)
```
universal_agent_architecture/
├── manifests/        ← FABRIC (Ontologies / Definitions)
├── graph/            ← GRAPH (State Machine OS)
├── task/             ← TASK (Durable Process + checkpoints)
├── router/           ← ROUTER (Decision Brain)
├── tools/            ← TOOLS (MCP / capability bus)
├── observer/         ← OBSERVER (OTel / tracing eyes)
├── memory/           ← Context management (working memory)
├── policy/           ← LAWS (OPA-style governance)
├── runtime/          ← API / execution layer
├── adapters/         ← NEXUS (protocol translation)
├── examples/         ← Reference implementations
└── infra/            ← Docker / deployment
```

### Architecture (Durable Agent OS)
- **GRAPH (The OS)**: Declarative, pausable, serializable state machines.
- **TASK (The Process)**: Durable work units that resume from checkpoints.
- **ROUTER (The Brain)**: Strategy layer for choosing the right model or rule path.
- **TOOLS (The Hands)**: Pluggable capabilities (MCP, HTTP, local functions).
- **OBSERVER (The Eyes)**: Native OpenTelemetry tracing of every transition.

Mermaid view:
```
graph TD
    API[REST API] --> Engine[Graph Engine]
    Engine --> Router[Router Handler]
    Engine --> Tools[Tool Handler]
    Engine --> Task[Task State]
    Router --> LLM[LLM / Model]
    Tools --> MCP[MCP Servers]
    Tools --> Local[Python Functions]
    Engine -.-> Observer[OTel Sink]
    Observer -.-> Jaeger[Jaeger / Honeycomb]
```

### Deep Structural Validation (Industry Parallels)
- **Separation of definition from execution**: `manifests/` vs `runtime/`.
- **Pluggable capabilities**: `tools/` + `adapters/` (MCP, LangGraph, AWS).
- **Observable state transitions**: `observer/` + `graph/` with OTel.
- **Durable work units**: `task/` with checkpointed progress.
- **Policy-driven governance**: `policy/` for OPA-style rules.

This is Kubernetes-for-Agents / Terraform-for-LLM-Workflows: the inevitable convergence point teams reach when making LLM systems reliable.

### 🔌 Extension Architecture (Zero Concrete Dependencies)

The kernel contains **no hardcoded implementations**. Every external dependency is behind an interface and injected at runtime via environment variables. This means you can wire UAA to AWS, GCP, Azure, on-prem, or anything else without modifying core code.

#### Core Contracts

All extension points implement abstract base classes defined in `universal_agent/contracts.py`:

```python
class ITaskStore(ABC):
    """Persist durable task state. Implement for: Postgres, DynamoDB, Redis, etc."""
    async def save_task(self, state: GraphState) -> None: ...
    async def get_task(self, execution_id: str) -> Optional[GraphState]: ...
    async def list_active_tasks(self) -> List[GraphState]: ...

class ITaskQueue(ABC):
    """Distribute work. Implement for: SQS, RabbitMQ, Redis Streams, etc."""
    async def enqueue(self, execution_id: str, priority: int = 0) -> None: ...
    async def dequeue(self) -> Optional[str]: ...

class IToolExecutor(ABC):
    """Execute capabilities. Implement for: MCP, Lambda, subprocess, HTTP, etc."""
    async def execute(self, config: Dict, arguments: Dict) -> Any: ...

class IRouterStrategy(ABC):
    """Model/tool selection. Implement for: OpenAI, Anthropic, Bedrock, rules, etc."""
    async def select_model(self, context: Dict, candidates: List[str]) -> str: ...
    async def select_tools(self, context: Dict, available: List[str]) -> List[str]: ...
```

Additionally, `BaseLLMClient` in `universal_agent/runtime/handlers.py` abstracts LLM providers:

```python
class BaseLLMClient(ABC):
    """LLM provider interface. Implement for: OpenAI, Anthropic, Bedrock, Ollama, etc."""
    async def chat(self, model: str, messages: List[Dict], tools: Optional[List] = None) -> Any: ...
```

#### Injection via Environment Variables

| Environment Variable | Interface | Default | Description |
|---------------------|-----------|---------|-------------|
| `UAA_TASK_STORE` | `ITaskStore` | `universal_agent.task.store.SQLTaskStore` | Where to persist task state |
| `UAA_TASK_QUEUE` | `ITaskQueue` | `universal_agent.task.queue.InMemoryTaskQueue` | How to distribute work |
| `UAA_LLM_CLIENT` | `BaseLLMClient` | `universal_agent.runtime.defaults.MockLLMClient` | Which LLM provider to use |
| `UAA_TOOL_EXECUTOR_LOCAL` | `IToolExecutor` | `universal_agent.runtime.defaults.MockToolExecutor` | Executor for `local` protocol tools |
| `UAA_TOOL_EXECUTOR_MCP` | `IToolExecutor` | `universal_agent.runtime.defaults.MockToolExecutor` | Executor for `mcp` protocol tools |
| `DATABASE_URL` | — | `sqlite+aiosqlite:///./local.db` | Connection string for SQLTaskStore |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | *(none)* | OpenTelemetry collector endpoint |

#### Example: Implementing a Custom Adapter

**1. Create your implementation:**
```python
# my_company/adapters/bedrock.py
from universal_agent.runtime.handlers import BaseLLMClient

class BedrockClient(BaseLLMClient):
    def __init__(self):
        import boto3
        self.client = boto3.client("bedrock-runtime")

    async def chat(self, model, messages, tools=None):
        # Your Bedrock implementation
        response = self.client.converse(modelId=model, messages=messages)
        return {"content": response["output"]["message"]["content"]}
```

**2. Create a DynamoDB task store:**
```python
# my_company/adapters/dynamo.py
from universal_agent.contracts import ITaskStore

class DynamoTaskStore(ITaskStore):
    def __init__(self, table_name: str):
        import boto3
        self.table = boto3.resource("dynamodb").Table(table_name)

    async def save_task(self, state):
        self.table.put_item(Item=state.model_dump(mode="json"))

    async def get_task(self, execution_id):
        resp = self.table.get_item(Key={"execution_id": execution_id})
        return GraphState(**resp["Item"]) if "Item" in resp else None

    async def list_active_tasks(self):
        # Scan for non-terminal states
        ...
```

**3. Run with your implementations:**
```bash
# Production deployment with custom adapters
UAA_LLM_CLIENT=my_company.adapters.bedrock.BedrockClient \
UAA_TASK_STORE=my_company.adapters.dynamo.DynamoTaskStore \
UAA_TOOL_EXECUTOR_MCP=adapters.mcp.client.MCPToolExecutor \
DATABASE_URL=dynamodb://tasks-table \
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317 \
uvicorn universal_agent.runtime.api:app --host 0.0.0.0
```

#### What Ships Out of the Box

| Component | Included Implementation | Production Alternative |
|-----------|------------------------|------------------------|
| Task Store | `SQLTaskStore` (SQLAlchemy async) | DynamoDB, Redis, Cosmos DB |
| Task Queue | `InMemoryTaskQueue` | SQS, RabbitMQ, Redis Streams |
| LLM Client | `MockLLMClient` (echo) | OpenAI, Anthropic, Bedrock, Ollama |
| Tool Executor | `MockToolExecutor` (passthrough) | `MCPToolExecutor`, Lambda, subprocess |
| Observer Sink | `OpenTelemetrySink` | Datadog, Honeycomb, custom |

The kernel remains untouched — you only implement interfaces and set environment variables.

### 🚀 Quick Start
1) **Prerequisites**
- Python 3.11+
- (Optional) Docker & Docker Compose

2) **Install**
```bash
git clone https://github.com/your-org/universal-agent-arch.git
cd universal-agent-arch

python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Unix:    source .venv/bin/activate

pip install -e .[dev]
```

3) **Create a Manifest (`manifest.yaml`)**
```yaml
name: "hello-world-agent"
version: "0.1.0"

graphs:
  - name: "main"
    entry_node: "start"
    nodes:
      - id: "start"
        kind: "router"
        router: { name: "greeter" }
      - id: "action"
        kind: "tool"
        tool: { name: "echo" }
    edges:
      - from_node: "start"
        to_node: "action"
        condition: { trigger: "success" }

routers:
  - name: "greeter"
    strategy: "llm"
    system_message: "You are a helpful assistant. Always use the 'echo' tool."

tools:
  - name: "echo"
    protocol: "local"
    description: "Echoes back text."
```

4) **Run the API**
```bash
uvicorn universal_agent.runtime.api:app --reload
```

5) **Spawn an Agent**
```bash
curl -X POST "http://127.0.0.1:8000/graphs/main/executions" \
     -H "Content-Type: application/json" \
     -d '{"input": {"query": "Hello world"}}'
```

### 🐳 Docker Stack (Recommended)
Run the full stack with Jaeger (for traces) and Postgres (for state).
```bash
docker-compose up -d
docker-compose ps
```
Access:
- Agent API: http://localhost:8000/docs
- Jaeger UI: http://localhost:16686

### 🛠 Advanced Usage

#### Human-in-the-Loop (HITL)
Define policies that require human approval for sensitive operations:
```yaml
policies:
  - name: "require-approval"
    rules:
      - action: "require_approval"
        target: ["tool:delete_db", "tool:deploy_prod"]
```

When a policy triggers, execution suspends. Resume via API:
```bash
curl -X POST "http://localhost:8000/executions/{id}/resume" \
     -H "Content-Type: application/json" \
     -d '{"input": {"approved": true, "feedback": "Looks good"}}'
```

#### Custom Tools via MCP
1. Implement `IToolExecutor` for MCP protocol (see `adapters/mcp/client.py` for reference)
2. Set `UAA_TOOL_EXECUTOR_MCP=your_module.MCPToolExecutor`
3. Define tools in your manifest with `protocol: "mcp"`

#### Custom LLM Providers
Implement `BaseLLMClient` and inject via `UAA_LLM_CLIENT`:
```python
class AnthropicClient(BaseLLMClient):
    async def chat(self, model, messages, tools=None):
        # Call Claude API
        ...
```

#### Production Persistence
Swap SQLite for Postgres/DynamoDB by implementing `ITaskStore`:
```bash
UAA_TASK_STORE=my_adapters.PostgresTaskStore \
DATABASE_URL=postgresql+asyncpg://user:pass@host/db \
uvicorn universal_agent.runtime.api:app
```

### 🤝 Contributing
- Fork the repository.
- Create a feature branch (`git checkout -b feature/amazing-feature`).
- Commit your changes (`git commit -m 'Add amazing feature'`).
- Push (`git push origin feature/amazing-feature`) and open a PR.

### 📜 License
Distributed under the MIT License. See `LICENSE` for details.


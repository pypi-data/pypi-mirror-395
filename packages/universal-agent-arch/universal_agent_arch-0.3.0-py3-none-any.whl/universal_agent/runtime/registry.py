"""
Contract Registry - Service Locator for UAA Infrastructure Components.

This module provides a centralized registry for contract implementations,
enabling dependency injection and runtime configuration of:
- Task stores (ITaskStore)
- Task queues (ITaskQueue)
- Tool executors (IToolExecutor)
- LLM clients (BaseLLMClient)
- Memory stores (IMemoryStore)

Usage:
    # Configure from environment or config file
    registry = ContractRegistry()
    registry.register_task_store(SQLTaskStore("postgresql://..."))
    registry.register_llm_client(OpenAIClient(api_key="..."))
    registry.register_tool_executor("mcp", MCPToolExecutor())
    
    # Use in runtime/handlers
    task_store = registry.get_task_store()
    executor = registry.get_tool_executor("mcp")
"""

from typing import Any, Dict, List, Optional, Type, TypeVar, Callable
import logging
import os
from abc import ABC

from universal_agent.contracts import ITaskStore, ITaskQueue, IToolExecutor

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RegistrationError(Exception):
    """Raised when registration fails."""
    pass


class ResolutionError(Exception):
    """Raised when a registered component cannot be resolved."""
    pass


class ContractRegistry:
    """
    Centralized registry for UAA contract implementations.
    
    This class implements the Service Locator pattern, providing a clean
    separation between interface definitions (contracts) and their
    concrete implementations.
    
    Thread Safety:
        This class is NOT thread-safe. For multi-threaded scenarios,
        configure the registry before starting worker threads.
    
    Attributes:
        _task_store: Registered ITaskStore implementation
        _task_queue: Registered ITaskQueue implementation
        _llm_client: Registered LLM client implementation
        _tool_executors: Dict of protocol -> IToolExecutor mappings
        _memory_stores: Dict of name -> memory store mappings
        _factories: Dict of lazy factory functions
    """
    
    def __init__(self):
        """Initialize an empty registry."""
        self._task_store: Optional[ITaskStore] = None
        self._task_queue: Optional[ITaskQueue] = None
        self._llm_client: Optional[Any] = None  # BaseLLMClient
        self._tool_executors: Dict[str, IToolExecutor] = {}
        self._memory_stores: Dict[str, Any] = {}
        self._observers: List[Any] = []
        
        # Lazy initialization factories
        self._factories: Dict[str, Callable[[], Any]] = {}
        
        # Type registrations for dynamic instantiation
        self._type_registry: Dict[str, Dict[str, Type]] = {
            "task_store": {},
            "task_queue": {},
            "tool_executor": {},
            "llm_client": {},
            "memory_store": {},
        }
    
    # --- Task Store ---
    
    def register_task_store(self, instance: ITaskStore) -> "ContractRegistry":
        """
        Register a task store implementation.
        
        Args:
            instance: ITaskStore implementation
            
        Returns:
            Self for method chaining
        """
        self._task_store = instance
        logger.info("Registered task store: %s", type(instance).__name__)
        return self
    
    def register_task_store_factory(self, factory: Callable[[], ITaskStore]) -> "ContractRegistry":
        """
        Register a lazy factory for task store.
        
        Args:
            factory: Callable that returns an ITaskStore
            
        Returns:
            Self for method chaining
        """
        self._factories["task_store"] = factory
        return self
    
    def get_task_store(self) -> ITaskStore:
        """
        Get the registered task store.
        
        Returns:
            Registered ITaskStore implementation
            
        Raises:
            ResolutionError: If no task store is registered
        """
        if self._task_store is None:
            # Try lazy factory
            if "task_store" in self._factories:
                self._task_store = self._factories["task_store"]()
            else:
                raise ResolutionError(
                    "No ITaskStore implementation registered. "
                    "Call register_task_store() or register_task_store_factory() first."
                )
        return self._task_store
    
    # --- Task Queue ---
    
    def register_task_queue(self, instance: ITaskQueue) -> "ContractRegistry":
        """
        Register a task queue implementation.
        
        Args:
            instance: ITaskQueue implementation
            
        Returns:
            Self for method chaining
        """
        self._task_queue = instance
        logger.info("Registered task queue: %s", type(instance).__name__)
        return self
    
    def get_task_queue(self) -> ITaskQueue:
        """
        Get the registered task queue.
        
        Returns:
            Registered ITaskQueue implementation
            
        Raises:
            ResolutionError: If no task queue is registered
        """
        if self._task_queue is None:
            if "task_queue" in self._factories:
                self._task_queue = self._factories["task_queue"]()
            else:
                raise ResolutionError(
                    "No ITaskQueue implementation registered. "
                    "Call register_task_queue() first."
                )
        return self._task_queue
    
    # --- Tool Executors ---
    
    def register_tool_executor(
        self,
        protocol: str,
        instance: IToolExecutor
    ) -> "ContractRegistry":
        """
        Register a tool executor for a specific protocol.
        
        Args:
            protocol: Protocol name (e.g., "mcp", "http", "local")
            instance: IToolExecutor implementation
            
        Returns:
            Self for method chaining
        """
        self._tool_executors[protocol] = instance
        logger.info("Registered tool executor for protocol '%s': %s", protocol, type(instance).__name__)
        return self
    
    def get_tool_executor(self, protocol: str) -> IToolExecutor:
        """
        Get a tool executor for a specific protocol.
        
        Args:
            protocol: Protocol name
            
        Returns:
            Registered IToolExecutor for the protocol
            
        Raises:
            ResolutionError: If no executor is registered for the protocol
        """
        if protocol not in self._tool_executors:
            # Try lazy factory
            factory_key = f"tool_executor:{protocol}"
            if factory_key in self._factories:
                self._tool_executors[protocol] = self._factories[factory_key]()
            else:
                available = list(self._tool_executors.keys())
                raise ResolutionError(
                    f"No IToolExecutor for protocol '{protocol}' registered. "
                    f"Available protocols: {available}"
                )
        return self._tool_executors[protocol]
    
    def get_all_tool_executors(self) -> Dict[str, IToolExecutor]:
        """Get all registered tool executors."""
        return self._tool_executors.copy()
    
    # --- LLM Client ---
    
    def register_llm_client(self, instance: Any) -> "ContractRegistry":
        """
        Register an LLM client implementation.
        
        Args:
            instance: BaseLLMClient implementation
            
        Returns:
            Self for method chaining
        """
        self._llm_client = instance
        logger.info("Registered LLM client: %s", type(instance).__name__)
        return self
    
    def get_llm_client(self) -> Any:
        """
        Get the registered LLM client.
        
        Returns:
            Registered LLM client implementation
            
        Raises:
            ResolutionError: If no LLM client is registered
        """
        if self._llm_client is None:
            if "llm_client" in self._factories:
                self._llm_client = self._factories["llm_client"]()
            else:
                raise ResolutionError(
                    "No LLM client implementation registered. "
                    "Call register_llm_client() first."
                )
        return self._llm_client
    
    # --- Memory Stores ---
    
    def register_memory_store(self, name: str, instance: Any) -> "ContractRegistry":
        """
        Register a memory store implementation.
        
        Args:
            name: Store name (matches MemoryStoreSpec.name)
            instance: Memory store implementation
            
        Returns:
            Self for method chaining
        """
        self._memory_stores[name] = instance
        logger.info("Registered memory store '%s': %s", name, type(instance).__name__)
        return self
    
    def get_memory_store(self, name: str) -> Any:
        """
        Get a memory store by name.
        
        Args:
            name: Store name
            
        Returns:
            Registered memory store
            
        Raises:
            ResolutionError: If no store is registered with that name
        """
        if name not in self._memory_stores:
            raise ResolutionError(
                f"No memory store registered with name '{name}'. "
                f"Available: {list(self._memory_stores.keys())}"
            )
        return self._memory_stores[name]
    
    # --- Observers ---
    
    def register_observer(self, instance: Any) -> "ContractRegistry":
        """
        Register an observer/telemetry sink.
        
        Args:
            instance: Observer implementation
            
        Returns:
            Self for method chaining
        """
        self._observers.append(instance)
        logger.info("Registered observer: %s", type(instance).__name__)
        return self
    
    def get_observers(self) -> List[Any]:
        """Get all registered observers."""
        return self._observers.copy()
    
    # --- Type Registration (for dynamic instantiation) ---
    
    def register_type(
        self,
        category: str,
        type_name: str,
        type_class: Type[T]
    ) -> "ContractRegistry":
        """
        Register a type for dynamic instantiation.
        
        Args:
            category: Component category (task_store, tool_executor, etc.)
            type_name: Type identifier (e.g., "sql", "dynamodb", "redis")
            type_class: The class to instantiate
            
        Returns:
            Self for method chaining
        """
        if category not in self._type_registry:
            self._type_registry[category] = {}
        self._type_registry[category][type_name] = type_class
        logger.debug("Registered type %s/%s: %s", category, type_name, type_class.__name__)
        return self
    
    def create_from_config(
        self,
        category: str,
        type_name: str,
        config: Dict[str, Any]
    ) -> Any:
        """
        Create an instance from a type registration.
        
        Args:
            category: Component category
            type_name: Registered type name
            config: Configuration dict to pass to constructor
            
        Returns:
            New instance of the registered type
            
        Raises:
            ResolutionError: If type is not registered
        """
        if category not in self._type_registry:
            raise ResolutionError(f"Unknown category: {category}")
        
        if type_name not in self._type_registry[category]:
            available = list(self._type_registry[category].keys())
            raise ResolutionError(
                f"Type '{type_name}' not registered in category '{category}'. "
                f"Available: {available}"
            )
        
        type_class = self._type_registry[category][type_name]
        return type_class(**config)
    
    # --- Configuration ---
    
    def configure_from_dict(self, config: Dict[str, Any]) -> "ContractRegistry":
        """
        Configure the registry from a configuration dictionary.
        
        Expected format:
        {
            "task_store": {"type": "sql", "connection_string": "..."},
            "task_queue": {"type": "sqs", "queue_url": "..."},
            "tool_executors": [
                {"protocol": "mcp", "type": "mcp_cli"},
                {"protocol": "http", "type": "http_requests"}
            ],
            "llm_client": {"type": "openai", "api_key": "..."},
        }
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Self for method chaining
        """
        # Task Store
        if "task_store" in config:
            ts_config = config["task_store"]
            type_name = ts_config.pop("type")
            instance = self.create_from_config("task_store", type_name, ts_config)
            self.register_task_store(instance)
        
        # Task Queue
        if "task_queue" in config:
            tq_config = config["task_queue"]
            type_name = tq_config.pop("type")
            instance = self.create_from_config("task_queue", type_name, tq_config)
            self.register_task_queue(instance)
        
        # Tool Executors
        if "tool_executors" in config:
            for exec_config in config["tool_executors"]:
                protocol = exec_config.pop("protocol")
                type_name = exec_config.pop("type")
                instance = self.create_from_config("tool_executor", type_name, exec_config)
                self.register_tool_executor(protocol, instance)
        
        # LLM Client
        if "llm_client" in config:
            llm_config = config["llm_client"]
            type_name = llm_config.pop("type")
            instance = self.create_from_config("llm_client", type_name, llm_config)
            self.register_llm_client(instance)
        
        return self
    
    def configure_from_env(self) -> "ContractRegistry":
        """
        Configure the registry from environment variables.
        
        Reads:
        - UAA_TASK_STORE: Dotted path to task store class
        - UAA_TASK_QUEUE: Dotted path to task queue class
        - UAA_LLM_CLIENT: Dotted path to LLM client class
        - UAA_TOOL_EXECUTOR_{PROTOCOL}: Dotted path to executor class
        
        Returns:
            Self for method chaining
        """
        # Task Store
        task_store_path = os.environ.get("UAA_TASK_STORE")
        if task_store_path:
            self._factories["task_store"] = lambda: self._import_and_instantiate(task_store_path)
        
        # Task Queue
        task_queue_path = os.environ.get("UAA_TASK_QUEUE")
        if task_queue_path:
            self._factories["task_queue"] = lambda: self._import_and_instantiate(task_queue_path)
        
        # LLM Client
        llm_client_path = os.environ.get("UAA_LLM_CLIENT")
        if llm_client_path:
            self._factories["llm_client"] = lambda: self._import_and_instantiate(llm_client_path)
        
        # Tool Executors (UAA_TOOL_EXECUTOR_MCP, UAA_TOOL_EXECUTOR_HTTP, etc.)
        for key, value in os.environ.items():
            if key.startswith("UAA_TOOL_EXECUTOR_"):
                protocol = key.replace("UAA_TOOL_EXECUTOR_", "").lower()
                # Capture value in closure
                self._factories[f"tool_executor:{protocol}"] = (
                    lambda v=value: self._import_and_instantiate(v)
                )
        
        return self
    
    def _import_and_instantiate(self, dotted_path: str) -> Any:
        """
        Import a class from a dotted path and instantiate it.
        
        Args:
            dotted_path: e.g., "mypackage.module.MyClass"
            
        Returns:
            Instance of the class
        """
        import importlib
        
        module_path, class_name = dotted_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls()
    
    # --- Utility ---
    
    def clear(self) -> "ContractRegistry":
        """Clear all registrations."""
        self._task_store = None
        self._task_queue = None
        self._llm_client = None
        self._tool_executors.clear()
        self._memory_stores.clear()
        self._observers.clear()
        self._factories.clear()
        return self
    
    def __repr__(self) -> str:
        return (
            f"ContractRegistry("
            f"task_store={type(self._task_store).__name__ if self._task_store else 'None'}, "
            f"task_queue={type(self._task_queue).__name__ if self._task_queue else 'None'}, "
            f"llm_client={type(self._llm_client).__name__ if self._llm_client else 'None'}, "
            f"tool_executors={list(self._tool_executors.keys())}, "
            f"memory_stores={list(self._memory_stores.keys())}"
            f")"
        )


# --- Global Registry (Singleton Pattern) ---

_global_registry: Optional[ContractRegistry] = None


def get_global_registry() -> ContractRegistry:
    """
    Get the global contract registry instance.
    
    Returns:
        The global ContractRegistry singleton
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = ContractRegistry()
    return _global_registry


def set_global_registry(registry: ContractRegistry) -> None:
    """
    Set the global contract registry instance.
    
    Args:
        registry: ContractRegistry to use as global
    """
    global _global_registry
    _global_registry = registry


__all__ = [
    "ContractRegistry",
    "RegistrationError",
    "ResolutionError",
    "get_global_registry",
    "set_global_registry",
]


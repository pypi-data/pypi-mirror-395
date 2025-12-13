"""
UAA Native Runtime - Execute Nexus manifests directly through the UAA kernel.

This runtime provides a direct execution path through the Universal Agent
Architecture's GraphEngine, without translating to LangGraph or AWS.

Usage:
    from universal_agent_nexus.adapters.uaa import UAANativeRuntime
    from universal_agent_architecture.task.store import SQLTaskStore
    from my_llm_client import MyLLMClient
    
    runtime = UAANativeRuntime(
        task_store=SQLTaskStore("postgresql://..."),
        llm_client=MyLLMClient(),
        tool_executors={"mcp": MCPToolExecutor()},
    )
    
    result = await runtime.execute(
        manifest=my_manifest,
        graph_name="main",
        input_data={"query": "Hello, world!"},
    )
"""

from typing import Any, Dict, List, Optional, Protocol
import uuid
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# --- Protocol Definitions (for type hinting without hard dependency) ---


class ITaskStore(Protocol):
    """Protocol for task persistence."""
    
    async def save_task(self, state: Any) -> None:
        """Persist the current state of a task."""
        ...
    
    async def get_task(self, execution_id: str) -> Optional[Any]:
        """Retrieve a task by ID."""
        ...


class IToolExecutor(Protocol):
    """Protocol for tool execution."""
    
    async def execute(self, config: Dict[str, Any], arguments: Dict[str, Any]) -> Any:
        """Run the tool and return output."""
        ...


class ILLMClient(Protocol):
    """Protocol for LLM providers."""
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None
    ) -> Any:
        """Send messages to the LLM and get a response."""
        ...


class IObserver(Protocol):
    """Protocol for observability."""
    
    def on_execution_start(self, state: Any) -> None:
        """Called when execution starts."""
        ...
    
    def on_step_start(self, state: Any, node_id: str, inputs: Dict[str, Any]) -> Any:
        """Called when a step starts. Returns a span/context object."""
        ...
    
    def on_step_end(self, span: Any, record: Any) -> None:
        """Called when a step ends."""
        ...


# --- UAA Native Runtime ---


class UAANativeRuntime:
    """
    Executes Nexus manifests directly through the UAA kernel.
    
    This runtime acts as the client-side orchestrator that drives the UAA
    GraphEngine. It handles dependency injection for task stores, LLM clients,
    and tool executors.
    
    Attributes:
        task_store: Implementation of ITaskStore for persistence
        llm_client: Implementation of ILLMClient for LLM calls
        tool_executors: Dict mapping protocol names to IToolExecutor instances
        observer: Optional observer for telemetry
    """
    
    def __init__(
        self,
        task_store: ITaskStore,
        llm_client: ILLMClient,
        tool_executors: Dict[str, IToolExecutor],
        observer: Optional[IObserver] = None,
        policy_engine: Optional[Any] = None,
    ):
        """
        Initialize the UAA Native Runtime.
        
        Args:
            task_store: Task persistence implementation
            llm_client: LLM client implementation
            tool_executors: Dict of protocol -> executor mappings
            observer: Optional telemetry observer
            policy_engine: Optional policy enforcement engine
        """
        self.task_store = task_store
        self.llm_client = llm_client
        self.tool_executors = tool_executors
        self.observer = observer
        self.policy_engine = policy_engine
        
        self._initialized = False
        self._manifest = None
    
    async def initialize(self, manifest: Any) -> None:
        """
        Initialize the runtime with a manifest.
        
        Args:
            manifest: AgentManifest to execute
        """
        self._manifest = manifest
        self._initialized = True
        logger.info("UAA Native Runtime initialized with manifest: %s", manifest.name)
    
    async def execute(
        self,
        manifest: Optional[Any] = None,
        graph_name: str = "main",
        input_data: Optional[Dict[str, Any]] = None,
        execution_id: Optional[str] = None,
        resume_from: Optional[str] = None,
    ) -> Any:
        """
        Execute a graph from the manifest using the UAA kernel's GraphEngine.
        
        Args:
            manifest: AgentManifest to execute (uses initialized manifest if None)
            graph_name: Name of the graph to execute
            input_data: Initial input data for the execution
            execution_id: Optional custom execution ID
            resume_from: Optional execution ID to resume from
            
        Returns:
            Final GraphState after execution
            
        Raises:
            ValueError: If graph not found or runtime not initialized
            RuntimeError: If execution fails
        """
        # Import UAA components (deferred to avoid import errors when UAA not installed)
        try:
            from universal_agent.graph.engine import GraphEngine
            from universal_agent.graph.model import Graph
            from universal_agent.graph.state import GraphState
            from universal_agent.runtime.handlers import RouterHandler, ToolHandler, HumanHandler
            from universal_agent.manifests.schema import GraphNodeKind
            from universal_agent.policy.engine import PolicyEngine
        except ImportError as e:
            raise ImportError(
                "universal-agent-arch is required for UAA native execution. "
                f"Install with: pip install universal-agent-arch. Error: {e}"
            )
        
        # Use provided manifest or initialized one
        manifest = manifest or self._manifest
        if manifest is None:
            raise ValueError("No manifest provided. Call initialize() first or pass manifest to execute().")
        
        # Find the graph
        graph_spec = next((g for g in manifest.graphs if g.name == graph_name), None)
        if not graph_spec:
            available = [g.name for g in manifest.graphs]
            raise ValueError(f"Graph '{graph_name}' not found in manifest. Available: {available}")
        
        # Build the graph model
        graph = Graph.from_spec(graph_spec)
        
        # Initialize or resume state
        if resume_from:
            state = await self.task_store.get_task(resume_from)
            if not state:
                raise ValueError(f"No task found with execution_id: {resume_from}")
            logger.info("Resuming execution from: %s", resume_from)
        else:
            state = GraphState(
                execution_id=execution_id or str(uuid.uuid4()),
                graph_name=graph_name,
                graph_version=graph_spec.version,
                context=input_data or {},
            )
            logger.info("Starting new execution: %s", state.execution_id)
        
        # Build policy engine if policies exist
        policy_engine = self.policy_engine
        if not policy_engine and manifest.policies:
            policy_engine = PolicyEngine(manifest.policies)
        
        # Build handlers with injected dependencies
        handlers = {
            GraphNodeKind.ROUTER: RouterHandler(
                manifest=manifest,
                llm_client=self.llm_client,
                policy_engine=policy_engine,
            ),
            GraphNodeKind.TOOL: ToolHandler(
                manifest=manifest,
                executors=self.tool_executors,
                policy_engine=policy_engine,
            ),
            GraphNodeKind.HUMAN: HumanHandler(state),
        }
        
        # Create and run the engine
        engine = GraphEngine(
            graph=graph,
            state=state,
            handlers=handlers,
            observer=self.observer,
        )
        
        # Notify observer of execution start
        if self.observer:
            self.observer.on_execution_start(state)
        
        try:
            await engine.run()
        except Exception as e:
            logger.error("Execution failed: %s", e, exc_info=True)
            state.fail(str(e))
        
        # Persist final state
        await self.task_store.save_task(state)
        
        logger.info(
            "Execution completed: %s, status: %s",
            state.execution_id,
            state.status
        )
        
        return state
    
    async def get_execution(self, execution_id: str) -> Optional[Any]:
        """
        Retrieve a previous execution by ID.
        
        Args:
            execution_id: The execution ID to retrieve
            
        Returns:
            GraphState if found, None otherwise
        """
        return await self.task_store.get_task(execution_id)
    
    async def list_active_executions(self) -> List[Any]:
        """
        List all active (non-terminal) executions.
        
        Returns:
            List of active GraphState instances
        """
        if hasattr(self.task_store, "list_active_tasks"):
            return await self.task_store.list_active_tasks()
        return []
    
    async def resume_execution(
        self,
        execution_id: str,
        human_input: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Resume a suspended execution.
        
        Args:
            execution_id: The execution ID to resume
            human_input: Optional input from human (for HITL nodes)
            
        Returns:
            Final GraphState after resumed execution
        """
        state = await self.task_store.get_task(execution_id)
        if not state:
            raise ValueError(f"No execution found with ID: {execution_id}")
        
        if state.status != "suspended":
            raise ValueError(f"Execution {execution_id} is not suspended (status: {state.status})")
        
        # Apply human input if provided
        if human_input:
            state.update_context(human_input)
            state.resume()
        
        # Re-execute from current position
        return await self.execute(
            manifest=self._manifest,
            graph_name=state.graph_name,
            resume_from=execution_id,
        )


class UAANativeRuntimeBuilder:
    """
    Builder pattern for constructing UAANativeRuntime instances.
    
    Usage:
        runtime = (UAANativeRuntimeBuilder()
            .with_task_store(SQLTaskStore("postgresql://..."))
            .with_llm_client(OpenAIClient(api_key="..."))
            .with_tool_executor("mcp", MCPToolExecutor())
            .with_tool_executor("http", HTTPToolExecutor())
            .with_observer(OpenTelemetrySink())
            .build())
    """
    
    def __init__(self):
        self._task_store: Optional[ITaskStore] = None
        self._llm_client: Optional[ILLMClient] = None
        self._tool_executors: Dict[str, IToolExecutor] = {}
        self._observer: Optional[IObserver] = None
        self._policy_engine: Optional[Any] = None
    
    def with_task_store(self, task_store: ITaskStore) -> "UAANativeRuntimeBuilder":
        """Set the task store implementation."""
        self._task_store = task_store
        return self
    
    def with_llm_client(self, llm_client: ILLMClient) -> "UAANativeRuntimeBuilder":
        """Set the LLM client implementation."""
        self._llm_client = llm_client
        return self
    
    def with_tool_executor(self, protocol: str, executor: IToolExecutor) -> "UAANativeRuntimeBuilder":
        """Add a tool executor for a specific protocol."""
        self._tool_executors[protocol] = executor
        return self
    
    def with_observer(self, observer: IObserver) -> "UAANativeRuntimeBuilder":
        """Set the telemetry observer."""
        self._observer = observer
        return self
    
    def with_policy_engine(self, policy_engine: Any) -> "UAANativeRuntimeBuilder":
        """Set the policy engine."""
        self._policy_engine = policy_engine
        return self
    
    def build(self) -> UAANativeRuntime:
        """
        Build the UAANativeRuntime instance.
        
        Returns:
            Configured UAANativeRuntime instance
            
        Raises:
            ValueError: If required components are missing
        """
        if self._task_store is None:
            raise ValueError("Task store is required. Call with_task_store() first.")
        
        if self._llm_client is None:
            raise ValueError("LLM client is required. Call with_llm_client() first.")
        
        return UAANativeRuntime(
            task_store=self._task_store,
            llm_client=self._llm_client,
            tool_executors=self._tool_executors,
            observer=self._observer,
            policy_engine=self._policy_engine,
        )


__all__ = [
    "UAANativeRuntime",
    "UAANativeRuntimeBuilder",
    "ITaskStore",
    "IToolExecutor",
    "ILLMClient",
    "IObserver",
]


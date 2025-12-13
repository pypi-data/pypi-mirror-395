"""
Base Runtime Class - SOLID Design

Eliminates boilerplate across all examples by providing:
- Single Responsibility: Handles only runtime setup/execution
- Open/Closed: Extensible via result extractors
- Liskov Substitution: Can be used anywhere runtime is needed
- Interface Segregation: Clean, focused API
- Dependency Inversion: Depends on abstractions (extractors, fabric)
"""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Callable, List
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
import logging

from langchain_core.messages import HumanMessage, BaseMessage
from universal_agent_nexus.compiler import parse
from universal_agent_nexus.ir.pass_manager import create_default_pass_manager, OptimizationLevel
from universal_agent_nexus.adapters.langgraph import LangGraphRuntime
from universal_agent_nexus.ir import ManifestIR

# Import observability from universal_agent_tools (promoted)
try:
    from universal_agent_tools.observability import setup_observability, trace_runtime_execution
except ImportError:
    # Fallback if not available
    def setup_observability(*args, **kwargs):
        return False
    
    @asynccontextmanager
    async def trace_runtime_execution(*args, **kwargs):
        yield

logger = logging.getLogger(__name__)


class ResultExtractor(ABC):
    """Abstract result extractor - Strategy pattern for different output formats."""
    
    @abstractmethod
    def extract(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract meaningful data from execution result.
        
        Args:
            result: Raw execution result from runtime
            
        Returns:
            Dict with extracted fields (decision, messages, execution_path, etc.)
        """
        pass


class MessagesStateExtractor(ResultExtractor):
    """Extract from MessagesState format (v3.0.0+)."""
    
    def extract(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract from messages and execution path."""
        messages = result.get("messages", [])
        executed_nodes = [k for k in result.keys() if k != "messages"]
        
        extracted = {
            "messages": messages,
            "execution_path": executed_nodes,
        }
        
        # Extract last message content if available
        if messages:
            last_message = messages[-1]
            if hasattr(last_message, "content"):
                extracted["last_content"] = str(last_message.content)
            elif isinstance(last_message, dict) and "content" in last_message:
                extracted["last_content"] = str(last_message["content"])
        
        return extracted


class ClassificationExtractor(ResultExtractor):
    """Extract classification result from messages."""
    
    def __init__(self, categories: Optional[List[str]] = None):
        """Initialize with expected categories."""
        self.categories = categories or []
    
    def extract(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract classification decision."""
        base = MessagesStateExtractor().extract(result)
        
        # Try to find classification in last content
        last_content = base.get("last_content", "").strip().lower()
        
        # Find matching category
        decision = None
        for cat in self.categories:
            if cat.lower() in last_content:
                decision = cat
                break
        
        base["decision"] = decision or last_content
        return base


class JSONExtractor(ResultExtractor):
    """Extract JSON data from LLM response."""
    
    def extract(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract JSON from messages."""
        base = MessagesStateExtractor().extract(result)
        
        import json
        import re
        
        # Search all messages for JSON, not just last
        messages = base.get("messages", [])
        for msg in messages:
            if hasattr(msg, "content"):
                content = str(msg.content)
            elif isinstance(msg, dict) and "content" in msg:
                content = str(msg["content"])
            else:
                continue
            
            # Try to find JSON in content
            if "{" in content:
                try:
                    json_start = content.find("{")
                    json_end = content.rfind("}") + 1
                    if json_end > json_start:
                        json_str = content[json_start:json_end]
                        # Normalize whitespace
                        json_str = re.sub(r'\s+', ' ', json_str.strip())
                        parsed = json.loads(json_str)
                        base["parsed_json"] = parsed
                        base["json_source"] = content  # Keep original for context
                        break
                except (json.JSONDecodeError, ValueError):
                    # Try ast.literal_eval as fallback
                    try:
                        import ast
                        dict_str = content[json_start:json_end]
                        base["parsed_json"] = ast.literal_eval(dict_str)
                        base["json_source"] = content
                        break
                    except:
                        pass
        
        return base


class NexusRuntime:
    """
    Base runtime class that eliminates boilerplate.
    
    Handles:
    - Manifest parsing and optimization
    - Runtime initialization
    - Observability setup
    - Execution with tracing
    - Result extraction (via strategy pattern)
    - Cache Fabric integration (optional)
    
    Example:
        ```python
        from universal_agent_nexus.runtime import NexusRuntime
        
        runtime = NexusRuntime(manifest_path="manifest.yaml")
        await runtime.setup()
        result = await runtime.execute("exec-001", {"messages": [...]})
        ```
    """
    
    def __init__(
        self,
        manifest_path: str = "manifest.yaml",
        graph_name: str = "main",
        service_name: Optional[str] = None,
        extractor: Optional[ResultExtractor] = None,
        enable_observability: bool = True,
        enable_checkpointing: bool = False,
        postgres_url: Optional[str] = None,
        opt_level: OptimizationLevel = OptimizationLevel.DEFAULT,
    ):
        """Initialize runtime.
        
        Args:
            manifest_path: Path to manifest.yaml
            graph_name: Graph name to initialize
            service_name: Service name for observability (defaults to graph_name)
            extractor: Result extractor strategy (defaults to MessagesStateExtractor)
            enable_observability: Enable OpenTelemetry tracing
            enable_checkpointing: Enable LangGraph checkpointing
            postgres_url: PostgreSQL URL for checkpointing
            opt_level: Optimization level for passes
        """
        self.manifest_path = Path(manifest_path)
        self.graph_name = graph_name
        self.service_name = service_name or graph_name
        self.extractor = extractor or MessagesStateExtractor()
        self.enable_observability = enable_observability
        self.opt_level = opt_level
        self.enable_checkpointing = enable_checkpointing
        self.postgres_url = postgres_url
        
        # Runtime components (initialized in setup)
        self.ir: Optional[ManifestIR] = None
        self.runtime: Optional[LangGraphRuntime] = None
        self.obs_enabled = False
        
        # Ensure parent directory is in path for imports
        parent_dir = self.manifest_path.parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
    
    async def setup(self) -> None:
        """Setup runtime: parse, optimize, initialize."""
        # Setup observability
        if self.enable_observability:
            self.obs_enabled = setup_observability(self.service_name)
        
        # Parse manifest
        logger.info(f"Parsing manifest: {self.manifest_path}")
        manifest_str = str(self.manifest_path)
        self.ir = parse(manifest_str)
        
        # Run optimization passes
        logger.info(f"Running optimization passes (level: {self.opt_level.name})")
        manager = create_default_pass_manager(self.opt_level)
        self.ir = manager.run(self.ir)
        
        # Log stats
        stats = manager.get_statistics()
        if stats:
            total_time = sum(s.elapsed_ms for s in stats.values())
            logger.info(f"Applied {len(stats)} passes in {total_time:.2f}ms")
        
        # Initialize runtime
        self.runtime = LangGraphRuntime(
            postgres_url=None if not self.enable_checkpointing else self.postgres_url,
            enable_checkpointing=self.enable_checkpointing,
        )
        await self.runtime.initialize(self.ir, graph_name=self.graph_name)
        logger.info(f"Runtime initialized for graph: {self.graph_name}")
    
    async def execute(
        self,
        execution_id: str,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute graph with tracing and result extraction.
        
        Args:
            execution_id: Unique execution identifier
            input_data: Input data (should include 'messages' for v3.0.0)
            config: Optional execution config
            
        Returns:
            Extracted result dict
        """
        if not self.runtime:
            raise RuntimeError("Runtime not initialized. Call setup() first.")
        
        # Ensure input_data has messages if not present
        if "messages" not in input_data:
            # Convert string to HumanMessage if needed
            if isinstance(input_data.get("content"), str):
                input_data["messages"] = [HumanMessage(content=input_data["content"])]
            elif "query" in input_data:
                input_data["messages"] = [HumanMessage(content=input_data["query"])]
        
        # Execute with tracing
        if self.obs_enabled:
            async with trace_runtime_execution(execution_id, graph_name=self.graph_name):
                raw_result = await self.runtime.execute(
                    execution_id=execution_id,
                    input_data=input_data,
                    config=config,
                )
        else:
            raw_result = await self.runtime.execute(
                execution_id=execution_id,
                input_data=input_data,
                config=config,
            )
        
        # Extract using strategy
        extracted = self.extractor.extract(raw_result)
        extracted["raw_result"] = raw_result  # Keep raw for debugging
        
        return extracted
    
    def create_input(self, content: str, **kwargs) -> Dict[str, Any]:
        """Helper to create MessagesState input.
        
        Args:
            content: Message content
            **kwargs: Additional state fields
            
        Returns:
            Input dict for execute()
        """
        return {
            "messages": [HumanMessage(content=content)],
            **kwargs,
        }


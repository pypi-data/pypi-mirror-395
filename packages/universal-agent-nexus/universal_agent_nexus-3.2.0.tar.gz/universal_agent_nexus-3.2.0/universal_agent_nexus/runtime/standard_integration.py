"""
Standard Integration Template - SOLID Design

Base class for all standardized examples with Cache Fabric + Output Parsers.
Follows SOLID principles:
- Single Responsibility: Handles only integration concerns
- Open/Closed: Extensible via composition
- Dependency Inversion: Depends on abstractions
"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import logging

from universal_agent_nexus.cache_fabric.base import CacheFabric, ContextScope
from universal_agent_nexus.cache_fabric.factory import create_cache_fabric
from universal_agent_nexus.cache_fabric.defaults import resolve_fabric_from_env
from universal_agent_nexus.cache_fabric.nexus_integration import store_manifest_contexts, get_router_prompt_from_fabric
from universal_agent_nexus.cache_fabric.runtime_integration import track_execution_with_fabric, record_feedback_to_fabric
from universal_agent_nexus.output_parsers import get_parser, OutputParser
from .runtime_base import NexusRuntime, ResultExtractor

logger = logging.getLogger(__name__)


class StandardExample(NexusRuntime):
    """
    Base class for all standardized examples.
    
    Provides:
    - Cache fabric initialization (memory/redis/vector)
    - Output parser integration
    - Manifest compilation and loading (via NexusRuntime)
    - Execution state tracking
    - Feedback recording
    
    This class follows the Template Method Pattern, providing a complete
    framework while allowing customization through inheritance.
    
    Example:
        ```python
        from universal_agent_nexus.runtime import StandardExample
        
        class MyExample(StandardExample):
            def __init__(self):
                super().__init__(
                    cache_backend="memory",
                    output_parser="classification",
                    manifest_path="manifest.yaml",
                    graph_name="main"
                )
            
            async def run(self):
                await self.setup()
                result = await self.execute("exec-001", {"messages": [...]})
                return result
        ```
    """
    
    def __init__(
        self,
        manifest_path: str = "manifest.yaml",
        graph_name: str = "main",
        cache_backend: Optional[str] = None,
        output_parser: Optional[str] = None,
        parser_config: Optional[Dict[str, Any]] = None,
        **runtime_kwargs,
    ):
        """Initialize standard example.
        
        Args:
            manifest_path: Path to manifest.yaml
            graph_name: Graph name to initialize
            cache_backend: 'memory', 'redis', or 'vector' (None = auto-detect from env)
            output_parser: Parser type ('classification', 'sentiment', etc)
            parser_config: Parser-specific configuration
            **runtime_kwargs: Additional args for NexusRuntime
        """
        super().__init__(
            manifest_path=manifest_path,
            graph_name=graph_name,
            service_name=graph_name,
            **runtime_kwargs,
        )
        
        self.parser_config = parser_config or {}
        
        # Initialize cache fabric (auto-detect from env if not specified)
        if cache_backend:
            self.fabric = create_cache_fabric(backend=cache_backend)
        else:
            self.fabric, _ = resolve_fabric_from_env()
        logger.info(f"Initialized cache fabric: {self.fabric.__class__.__name__}")
        
        # Initialize output parser
        self.parser: Optional[OutputParser] = None
        if output_parser:
            self.parser = get_parser(output_parser, **self.parser_config)
            logger.info(f"Initialized parser: {output_parser}")
    
    async def setup(self) -> None:
        """Setup runtime and cache manifest contexts."""
        # Setup base runtime
        await super().setup()
        
        # Store manifest contexts in fabric
        if self.ir and self.fabric:
            await store_manifest_contexts(
                manifest=self.ir,
                fabric=self.fabric,
                graph_name=self.graph_name,
            )
            logger.info("Stored manifest contexts in Cache Fabric")
    
    async def execute(
        self,
        execution_id: str,
        input_data: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None,
        track_in_fabric: bool = True,
    ) -> Dict[str, Any]:
        """Execute with fabric tracking and optional parsing.
        
        Args:
            execution_id: Unique execution identifier
            input_data: Input data
            config: Optional execution config
            track_in_fabric: Whether to track execution in fabric
            
        Returns:
            Extracted result dict (with parsed output if parser configured)
        """
        # Execute via base class
        result = await super().execute(execution_id, input_data, config)
        
        # Parse output if parser configured
        if self.parser and "last_content" in result:
            parsed = self.parser.parse(result["last_content"])
            result["parsed"] = parsed.parsed if parsed.success else None
            result["parse_confidence"] = parsed.confidence
        
        # Track in fabric
        if track_in_fabric and self.fabric:
            await track_execution_with_fabric(
                execution_id=execution_id,
                graph_name=self.graph_name,
                result=result.get("raw_result", result),
                fabric=self.fabric,
            )
        
        return result
    
    async def get_system_prompt(self, router_name: str, default: Optional[str] = None) -> Optional[str]:
        """Get system prompt from cache fabric.
        
        Args:
            router_name: Router name
            default: Default prompt if not found
            
        Returns:
            System prompt or None
        """
        if not self.fabric:
            return default
        
        return await get_router_prompt_from_fabric(
            router_name=router_name,
            fabric=self.fabric,
            default=default,
        )
    
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> None:
        """Record feedback for execution.
        
        Args:
            execution_id: Execution identifier
            feedback: Feedback data (rating, corrections, etc)
        """
        if not self.fabric:
            logger.warning("No fabric configured, cannot record feedback")
            return
        
        await record_feedback_to_fabric(
            execution_id=execution_id,
            feedback=feedback,
            fabric=self.fabric,
        )
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get execution metrics from fabric.
        
        Returns:
            Metrics dict
        """
        if not self.fabric:
            return {}
        
        return await self.fabric.get_metrics()


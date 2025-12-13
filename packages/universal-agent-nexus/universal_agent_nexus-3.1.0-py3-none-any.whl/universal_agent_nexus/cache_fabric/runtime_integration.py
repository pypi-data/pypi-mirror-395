"""Agent runtime integration - Read from fabric and track execution state."""

from typing import Dict, Any, Optional
from universal_agent_nexus.adapters.langgraph import LangGraphRuntime

from .base import CacheFabric, ContextScope


class FabricAwareRuntime:
    """Wrapper around LangGraphRuntime that integrates with Cache Fabric."""
    
    def __init__(
        self,
        runtime: LangGraphRuntime,
        fabric: CacheFabric,
    ):
        self.runtime = runtime
        self.fabric = fabric
    
    async def execute(
        self,
        execution_id: str,
        input_data: Dict[str, Any],
        graph_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute with fabric integration.
        
        - Reads system prompts from fabric (hot-reload)
        - Tracks execution state
        - Records feedback
        
        Args:
            execution_id: Unique execution identifier
            input_data: Input data for execution
            graph_name: Optional graph name
        
        Returns:
            Execution result
        """
        # Execute
        result = await self.runtime.execute(
            execution_id=execution_id,
            input_data=input_data,
        )
        
        # Track execution state
        await self.fabric.track_execution(
            execution_id=execution_id,
            graph_name=graph_name or "main",
            state={
                "input": input_data,
                "output": result,
                "nodes_executed": [k for k in result.keys() if k != "messages"],
            },
        )
        
        return result
    
    async def record_feedback(
        self,
        execution_id: str,
        feedback: Dict[str, Any],
    ) -> None:
        """Record feedback for an execution.
        
        Args:
            execution_id: Execution identifier
            feedback: Feedback data (status, classification, user_rating, etc.)
        """
        await self.fabric.record_feedback(execution_id, feedback)


async def track_execution_with_fabric(
    execution_id: str,
    graph_name: str,
    result: Dict[str, Any],
    fabric: CacheFabric,
) -> None:
    """Helper to track execution state in fabric.
    
    Args:
        execution_id: Execution identifier
        graph_name: Graph name
        result: Execution result
        fabric: Cache Fabric instance
    """
    await fabric.track_execution(
        execution_id=execution_id,
        graph_name=graph_name,
        state={
            "output": result,
            "nodes_executed": [k for k in result.keys() if k != "messages"],
        },
    )


async def record_feedback_to_fabric(
    execution_id: str,
    feedback: Dict[str, Any],
    fabric: CacheFabric,
) -> None:
    """Helper to record feedback in fabric.
    
    Args:
        execution_id: Execution identifier
        feedback: Feedback data
        fabric: Cache Fabric instance
    """
    await fabric.record_feedback(execution_id, feedback)


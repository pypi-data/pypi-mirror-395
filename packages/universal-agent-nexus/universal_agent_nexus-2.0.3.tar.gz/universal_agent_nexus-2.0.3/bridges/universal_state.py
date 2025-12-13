"""
Normalized state representation shared across adapters.

This module provides a bidirectional bridge to translate state from any supported
runtime (LangGraph, AWS Step Functions) into the Universal Agent Architecture's (UAA)
canonical GraphState format, and back again.

Pipeline:
    LangGraph Checkpoint  ─┐
                           ├─► normalize() ─► NormalizedGraphState ─► denormalize() ─► Target Format
    AWS Step Functions   ──┘

This enables:
- Cross-runtime state synchronization
- Debugging and inspection across environments
- State migration between runtimes
- Unified observability
"""

from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import json
from datetime import datetime


# --- Canonical UAA Models ---


class NormalizedHistoryEntry(BaseModel):
    """
    A canonical representation of a single step in a graph's execution history.
    
    This model captures all the essential information about a node execution,
    regardless of which runtime produced it.
    """
    node_id: str = Field(..., description="Unique identifier of the executed node")
    node_kind: str = Field(..., description="Type of node: 'router', 'tool', 'task', 'human'")
    status: str = Field(..., description="Execution status: 'completed', 'failed', 'running', 'skipped'")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input passed to the node")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Output produced by the node")
    error: Optional[str] = Field(default=None, description="Error message if status is 'failed'")
    started_at: str = Field(..., description="ISO8601 timestamp when execution started")
    ended_at: Optional[str] = Field(default=None, description="ISO8601 timestamp when execution ended")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional runtime-specific metadata")


class NormalizedGraphState(BaseModel):
    """
    The canonical UAA GraphState format.
    
    This is the universal representation that all runtime states normalize to.
    It preserves execution history, context, and status information.
    """
    execution_id: str = Field(..., description="Unique execution identifier")
    graph_name: str = Field(..., description="Name of the graph being executed")
    status: str = Field(..., description="Overall execution status: 'pending', 'running', 'completed', 'failed', 'suspended'")
    context: Dict[str, Any] = Field(default_factory=dict, description="Current execution context/state")
    history: List[NormalizedHistoryEntry] = Field(default_factory=list, description="Ordered list of executed steps")
    current_node_id: Optional[str] = Field(default=None, description="Currently executing node ID")
    version: str = Field(default="1.0.0", description="State schema version")
    graph_version: Optional[str] = Field(default=None, description="Version of the graph definition")
    created_at: Optional[str] = Field(default=None, description="ISO8601 timestamp when execution started")
    updated_at: Optional[str] = Field(default=None, description="ISO8601 timestamp of last update")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        extra = "allow"


# --- Runtime Format Detection ---


class StateFormat(str, Enum):
    """Supported runtime state formats."""
    UAA = "uaa"
    LANGGRAPH = "langgraph"
    AWS = "aws"


def detect_format(state: dict) -> StateFormat:
    """
    Detect the source format of a state dict.
    
    Args:
        state: The state dictionary to analyze
        
    Returns:
        StateFormat enum indicating the detected format
        
    Raises:
        ValueError: If the format cannot be determined
    """
    # UAA native format
    if "execution_id" in state and "graph_name" in state and "history" in state:
        return StateFormat.UAA
    
    # LangGraph checkpoint format - has channel_values or values with configurable
    if "channel_values" in state or ("values" in state and "configurable" in state.get("config", {})):
        return StateFormat.LANGGRAPH
    
    # LangGraph simplified format (thread_id based)
    if "thread_id" in state or ("config" in state and "thread_id" in state.get("config", {})):
        return StateFormat.LANGGRAPH
    
    # AWS Step Functions format
    if "executionArn" in state or "stateMachineArn" in state:
        return StateFormat.AWS
    
    # Check for AWS event history format
    if isinstance(state, dict) and state.get("status") in ["RUNNING", "SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"]:
        return StateFormat.AWS
    
    raise ValueError(f"Unknown state format. Keys present: {list(state.keys())[:10]}")


# --- Normalization Functions ---


def normalize(
    state: dict,
    history_events: Optional[List[dict]] = None,
    source_format: Optional[StateFormat] = None
) -> NormalizedGraphState:
    """
    Normalize state from any runtime to UAA GraphState format.
    
    Args:
        state: The state object from the source runtime
        history_events: Optional list of history events (required for AWS)
        source_format: Optional explicit format (auto-detected if not provided)
        
    Returns:
        NormalizedGraphState with all available information preserved
        
    Raises:
        ValueError: If format cannot be detected or required data is missing
    """
    fmt = source_format or detect_format(state)
    
    if fmt == StateFormat.UAA:
        return _normalize_uaa(state)
    elif fmt == StateFormat.LANGGRAPH:
        return _normalize_langgraph(state)
    elif fmt == StateFormat.AWS:
        if history_events is None:
            raise ValueError("`history_events` are required to normalize AWS state.")
        return _normalize_aws(state, history_events)
    
    raise NotImplementedError(f"Normalization for {fmt} not implemented.")


def _normalize_uaa(state: dict) -> NormalizedGraphState:
    """Convert UAA native state to NormalizedGraphState."""
    # Already in UAA format, just validate and convert
    history = []
    for entry in state.get("history", []):
        if isinstance(entry, dict):
            history.append(NormalizedHistoryEntry(**entry))
        elif hasattr(entry, "model_dump"):
            history.append(NormalizedHistoryEntry(**entry.model_dump()))
    
    return NormalizedGraphState(
        execution_id=state["execution_id"],
        graph_name=state["graph_name"],
        status=state.get("status", "pending"),
        context=state.get("context", {}),
        history=history,
        current_node_id=state.get("current_node_id"),
        version=state.get("version", "1.0.0"),
        graph_version=state.get("graph_version"),
        created_at=state.get("created_at"),
        updated_at=state.get("updated_at"),
        metadata=state.get("metadata", {}),
    )


def _normalize_langgraph(checkpoint: dict) -> NormalizedGraphState:
    """
    Convert LangGraph checkpoint to UAA format.
    
    LangGraph stores state in channel_values and tracks history through
    message history. This function extracts and normalizes that information.
    """
    config = checkpoint.get("config", {})
    configurable = config.get("configurable", config)
    
    # Extract values from either channel_values or values
    values = checkpoint.get("channel_values", checkpoint.get("values", {}))
    
    # Extract thread/execution ID
    execution_id = (
        configurable.get("thread_id") or 
        checkpoint.get("thread_id") or 
        "unknown"
    )
    
    # Extract graph name from metadata or default
    graph_name = checkpoint.get("graph_name", "main")
    
    # Build history from messages if available
    history = _extract_langgraph_history(values, checkpoint)
    
    # Determine current node from checkpoint metadata
    current_node = None
    if "next" in checkpoint:
        next_nodes = checkpoint["next"]
        if isinstance(next_nodes, list) and next_nodes:
            current_node = next_nodes[0]
        elif isinstance(next_nodes, str):
            current_node = next_nodes
    
    # Determine status
    status = "running"
    if checkpoint.get("next") == [] or checkpoint.get("next") is None:
        status = "completed"
    
    # Extract timestamps
    ts = checkpoint.get("ts")
    created_at = ts if ts else datetime.utcnow().isoformat()
    
    return NormalizedGraphState(
        execution_id=str(execution_id),
        graph_name=graph_name,
        status=status,
        context=values,
        history=history,
        current_node_id=current_node,
        version="1.0.0",
        created_at=created_at,
        updated_at=created_at,
        metadata={
            "source": "langgraph",
            "checkpoint_id": checkpoint.get("id"),
            "parent_id": checkpoint.get("parent_id"),
        },
    )


def _extract_langgraph_history(values: dict, checkpoint: dict) -> List[NormalizedHistoryEntry]:
    """
    Extract execution history from LangGraph checkpoint.
    
    LangGraph stores history implicitly in message lists and tool call records.
    This function reconstructs the node execution history from that data.
    """
    history = []
    messages = values.get("messages", [])
    
    for i, msg in enumerate(messages):
        # Handle different message formats
        if isinstance(msg, dict):
            role = msg.get("role", msg.get("type", "unknown"))
            content = msg.get("content", "")
            name = msg.get("name")
            tool_calls = msg.get("tool_calls", [])
        elif hasattr(msg, "type"):
            role = getattr(msg, "type", "unknown")
            content = getattr(msg, "content", "")
            name = getattr(msg, "name", None)
            tool_calls = getattr(msg, "tool_calls", [])
        else:
            continue
        
        # Create history entry based on message type
        node_kind = "task"
        if role == "tool" or name:
            node_kind = "tool"
        elif tool_calls:
            node_kind = "router"
        
        entry = NormalizedHistoryEntry(
            node_id=name or f"step_{i}",
            node_kind=node_kind,
            status="completed",
            input_data={"content": content} if role == "user" else {},
            output_data={"content": content} if role != "user" else None,
            started_at=datetime.utcnow().isoformat(),
            ended_at=datetime.utcnow().isoformat(),
            metadata={"role": role, "index": i},
        )
        history.append(entry)
    
    return history


def _normalize_aws(execution_details: dict, history_events: List[dict]) -> NormalizedGraphState:
    """
    Convert AWS Step Functions state and history to UAA format.
    
    AWS provides execution details and a separate event history. This function
    correlates the events to build a coherent execution history.
    """
    history = []
    node_map: Dict[int, NormalizedHistoryEntry] = {}
    
    for event in history_events:
        event_type = event.get("type", "")
        event_id = event.get("id", 0)
        timestamp = event.get("timestamp")
        
        # Handle timestamp formatting
        if timestamp:
            if hasattr(timestamp, "isoformat"):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)
        else:
            timestamp = datetime.utcnow().isoformat()
        
        # State entered events
        if event_type == "TaskStateEntered":
            details = event.get("stateEnteredEventDetails", {})
            node_id = details.get("name", f"node_{event_id}")
            input_str = details.get("input", "{}")
            
            try:
                input_data = json.loads(input_str) if isinstance(input_str, str) else input_str
            except json.JSONDecodeError:
                input_data = {"raw": input_str}
            
            node_map[event_id] = NormalizedHistoryEntry(
                node_id=node_id,
                node_kind="task",
                status="running",
                input_data=input_data,
                started_at=timestamp,
                metadata={"aws_event_id": event_id},
            )
        
        # State exited events (success)
        elif event_type == "TaskStateExited":
            details = event.get("stateExitedEventDetails", {})
            prev_id = event.get("previousEventId")
            entry = node_map.get(prev_id)
            
            if entry:
                output_str = details.get("output", "{}")
                try:
                    output_data = json.loads(output_str) if isinstance(output_str, str) else output_str
                except json.JSONDecodeError:
                    output_data = {"raw": output_str}
                
                entry.status = "completed"
                entry.output_data = output_data
                entry.ended_at = timestamp
        
        # Task failed events
        elif event_type == "TaskFailed":
            details = event.get("taskFailedEventDetails", {})
            prev_id = event.get("previousEventId")
            entry = node_map.get(prev_id)
            
            if entry:
                entry.status = "failed"
                entry.error = details.get("error", "Unknown error")
                entry.ended_at = timestamp
                entry.metadata["cause"] = details.get("cause")
        
        # Lambda function events
        elif event_type == "LambdaFunctionScheduled":
            details = event.get("lambdaFunctionScheduledEventDetails", {})
            node_map[event_id] = NormalizedHistoryEntry(
                node_id=details.get("resource", f"lambda_{event_id}"),
                node_kind="tool",
                status="running",
                input_data=json.loads(details.get("input", "{}")),
                started_at=timestamp,
                metadata={"aws_event_id": event_id, "function_arn": details.get("resource")},
            )
        
        elif event_type == "LambdaFunctionSucceeded":
            details = event.get("lambdaFunctionSucceededEventDetails", {})
            prev_id = event.get("previousEventId")
            entry = node_map.get(prev_id)
            
            if entry:
                entry.status = "completed"
                entry.output_data = json.loads(details.get("output", "{}"))
                entry.ended_at = timestamp
        
        elif event_type == "LambdaFunctionFailed":
            details = event.get("lambdaFunctionFailedEventDetails", {})
            prev_id = event.get("previousEventId")
            entry = node_map.get(prev_id)
            
            if entry:
                entry.status = "failed"
                entry.error = details.get("error", "Lambda execution failed")
                entry.ended_at = timestamp

    # Convert node_map to ordered list
    history = list(node_map.values())
    
    # Map AWS status to UAA status
    aws_status = execution_details.get("status", "UNKNOWN")
    status_map = {
        "RUNNING": "running",
        "SUCCEEDED": "completed",
        "FAILED": "failed",
        "TIMED_OUT": "failed",
        "ABORTED": "failed",
    }
    status = status_map.get(aws_status, "pending")
    
    # Parse execution ARN for IDs
    execution_arn = execution_details.get("executionArn", "")
    state_machine_arn = execution_details.get("stateMachineArn", "")
    
    execution_id = execution_arn.split(":")[-1] if execution_arn else "unknown"
    graph_name = state_machine_arn.split(":")[-1] if state_machine_arn else "unknown"
    
    # Parse input
    input_str = execution_details.get("input", "{}")
    try:
        context = json.loads(input_str) if isinstance(input_str, str) else input_str
    except json.JSONDecodeError:
        context = {"raw": input_str}
    
    # Parse timestamps
    start_date = execution_details.get("startDate")
    stop_date = execution_details.get("stopDate")
    
    if start_date and hasattr(start_date, "isoformat"):
        start_date = start_date.isoformat()
    if stop_date and hasattr(stop_date, "isoformat"):
        stop_date = stop_date.isoformat()
    
    return NormalizedGraphState(
        execution_id=execution_id,
        graph_name=graph_name,
        status=status,
        context=context,
        history=history,
        current_node_id=history[-1].node_id if history else None,
        version="1.0.0",
        created_at=str(start_date) if start_date else None,
        updated_at=str(stop_date) if stop_date else None,
        metadata={
            "source": "aws_step_functions",
            "execution_arn": execution_arn,
            "state_machine_arn": state_machine_arn,
        },
    )


# --- Denormalization Functions ---


def denormalize(state: NormalizedGraphState, target: StateFormat) -> dict:
    """
    Convert UAA GraphState to target runtime format.
    
    Args:
        state: The normalized graph state
        target: The target format to convert to
        
    Returns:
        Dictionary in the target runtime's format
    """
    if target == StateFormat.LANGGRAPH:
        return _denormalize_to_langgraph(state)
    elif target == StateFormat.AWS:
        return _denormalize_to_aws(state)
    elif target == StateFormat.UAA:
        return state.model_dump(exclude_none=True)
    
    raise NotImplementedError(f"Denormalization to {target} not implemented.")


def _denormalize_to_langgraph(state: NormalizedGraphState) -> dict:
    """Convert NormalizedGraphState to LangGraph checkpoint format."""
    # Reconstruct messages from history
    messages = []
    for entry in state.history:
        if entry.node_kind == "router":
            # AI/assistant message
            msg = {
                "type": "ai",
                "content": entry.output_data.get("content", "") if entry.output_data else "",
                "name": entry.node_id,
            }
            if entry.output_data and "tool_calls" in entry.output_data:
                msg["tool_calls"] = entry.output_data["tool_calls"]
            messages.append(msg)
        elif entry.node_kind == "tool":
            # Tool response message
            messages.append({
                "type": "tool",
                "content": json.dumps(entry.output_data) if entry.output_data else "",
                "name": entry.node_id,
            })
        elif entry.input_data.get("content"):
            # User message
            messages.append({
                "type": "human",
                "content": entry.input_data["content"],
            })
    
    return {
        "config": {
            "configurable": {
                "thread_id": state.execution_id,
            }
        },
        "channel_values": {
            **state.context,
            "messages": messages,
        },
        "next": [state.current_node_id] if state.current_node_id else [],
        "ts": state.updated_at or state.created_at,
    }


def _denormalize_to_aws(state: NormalizedGraphState) -> dict:
    """Convert NormalizedGraphState to AWS Step Functions input format."""
    # AWS denormalization is typically just providing input for a new execution
    # The history cannot be "restored" in AWS - it's immutable
    return {
        "input": json.dumps(state.context),
        "name": f"{state.graph_name}-{state.execution_id}",
        "stateMachineArn": state.metadata.get("state_machine_arn", ""),
    }


# --- Utility Functions ---


def sync_state(
    source_state: dict,
    source_format: StateFormat,
    target_format: StateFormat,
    history_events: Optional[List[dict]] = None,
) -> dict:
    """
    Convenience function to sync state from one runtime to another.
    
    Args:
        source_state: State from source runtime
        source_format: Format of source state
        target_format: Desired target format
        history_events: Required for AWS source format
        
    Returns:
        State in target format
    """
    normalized = normalize(source_state, history_events, source_format)
    return denormalize(normalized, target_format)


__all__ = [
    # Models
    "NormalizedHistoryEntry",
    "NormalizedGraphState",
    # Enums
    "StateFormat",
    # Functions
    "detect_format",
    "normalize",
    "denormalize",
    "sync_state",
]

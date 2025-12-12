"""
AWS Step Functions adapter for Universal Agent Architecture.

Compiles UAA graphs → Amazon States Language (ASL) with:
- Choice states for routing
- Task states for Lambda invocation
- Map states for parallel execution
- Error handling with Retry/Catch
- JSONPath for data flow
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from universal_agent.manifests.schema import (
    AgentManifest,
    GraphSpec,
    GraphNodeKind,
    EdgeTrigger,
    EdgeCondition,
)

logger = logging.getLogger(__name__)


class StepFunctionsCompiler:
    """
    Compile UAA graphs to AWS Step Functions State Machine definitions (ASL).

    December 2025 Best Practices:
    - JSONata expressions for Choice conditions
    - Exponential backoff for retries
    - Catch blocks for error routing
    - ResultPath for state isolation
    """

    def __init__(
        self,
        lambda_prefix: str = "uaa",
        region: str = "us-east-1",
        account_id: Optional[str] = None,
    ):
        self.lambda_prefix = lambda_prefix
        self.region = region
        self.account_id = account_id or "123456789012"  # Placeholder

    def compile(self, manifest: AgentManifest, graph_name: str = "main") -> dict:
        """
        Compile UAA manifest → ASL state machine definition.

        Returns:
            dict: ASL-compliant state machine definition
        """
        graph = self._find_graph(manifest, graph_name)
        if not graph:
            raise ValueError(f"Graph '{graph_name}' not found in manifest")

        logger.info("Compiling graph '%s' to Step Functions ASL", graph_name)

        states = self._compile_nodes_to_states(graph, manifest)

        asl = {
            "Comment": f"UAA Graph: {manifest.name} v{manifest.version} - {graph.description or graph_name}",
            "StartAt": graph.entry_node,
            "States": states,
            "TimeoutSeconds": self._get_graph_timeout(graph),
        }

        logger.info("[OK] Compiled %d states for graph '%s'", len(states), graph_name)
        return asl

    def _find_graph(self, manifest: AgentManifest, graph_name: str) -> Optional[GraphSpec]:
        """Find graph by name in manifest."""
        return next((g for g in manifest.graphs if g.name == graph_name), None)

    def _compile_nodes_to_states(
        self, graph: GraphSpec, manifest: AgentManifest
    ) -> Dict[str, Any]:
        """
        Map UAA nodes → ASL states.

        Node types:
        - router → Choice state
        - task → Task state (Lambda)
        - tool → Task state (Lambda with tool invocation)
        """
        states = {}

        for node in graph.nodes:
            if node.kind == GraphNodeKind.ROUTER:
                states[node.id] = self._create_choice_state(node, graph)
            elif node.kind == GraphNodeKind.TASK:
                states[node.id] = self._create_task_state(node, graph)
            elif node.kind == GraphNodeKind.TOOL:
                states[node.id] = self._create_tool_state(node, graph, manifest)
            else:
                logger.warning("Unsupported node kind: %s (node=%s)", node.kind, node.id)
                states[node.id] = self._create_pass_state(node)

        return states

    def _create_choice_state(self, node, graph: GraphSpec) -> dict:
        """
        UAA router node → ASL Choice state.

        Uses JSONata expressions for conditions.
        """
        outgoing_edges = [e for e in graph.edges if e.from_node == node.id]

        if not outgoing_edges:
            logger.warning("Router node %s has no outgoing edges", node.id)
            return {"Type": "Succeed"}

        choices = []
        default_next = None

        for edge in outgoing_edges:
            condition = (
                edge.condition
                if edge.condition
                else EdgeCondition(trigger=EdgeTrigger.SUCCESS)
            )

            if condition.trigger == EdgeTrigger.SUCCESS:
                default_next = edge.to_node
            elif condition.trigger == EdgeTrigger.ERROR:
                choices.append({
                    "Condition": "{% $.error != null %}",
                    "Next": edge.to_node,
                })
            elif hasattr(condition, "expression") and condition.expression:
                choices.append({
                    "Condition": f"{{% {condition.expression} %}}",
                    "Next": edge.to_node,
                })

        state: Dict[str, Any] = {"Type": "Choice", "Choices": choices}

        if default_next:
            state["Default"] = default_next

        return state

    def _create_task_state(self, node, graph: GraphSpec) -> dict:
        """
        UAA task node → ASL Task state (Lambda invocation).

        Production patterns:
        - Exponential backoff retry
        - Catch for error routing
        - ResultPath to preserve input
        """
        lambda_arn = self._build_lambda_arn(node.id)

        state: Dict[str, Any] = {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Parameters": {
                "FunctionName": lambda_arn,
                "Payload": {
                    "node_id.$": "$.current_node",
                    "context.$": "$.context",
                    "execution_id.$": "$.execution_id",
                },
            },
            "ResultPath": "$.task_result",
            "Retry": self._build_retry_config(node),
        }

        catch_config = self._build_catch_config(node, graph)
        if catch_config:
            state["Catch"] = catch_config

        next_state = self._find_next_state(node, graph, EdgeTrigger.SUCCESS)
        if next_state:
            state["Next"] = next_state
        else:
            state["End"] = True

        return state

    def _create_tool_state(
        self, node, graph: GraphSpec, manifest: AgentManifest
    ) -> dict:
        """
        UAA tool node → ASL Task state with tool invocation.

        Tools are Lambda functions that wrap MCP/HTTP/subprocess calls.
        """
        tool_ref = node.tool
        tool_name = tool_ref.name if tool_ref else node.id
        lambda_arn = self._build_lambda_arn(f"tool-{tool_name}")

        state: Dict[str, Any] = {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "Parameters": {
                "FunctionName": lambda_arn,
                "Payload": {
                    "tool_name": tool_name,
                    "tool_input.$": "$.context.tool_input",
                    "context.$": "$.context",
                },
            },
            "ResultPath": "$.tool_result",
            "Retry": self._build_retry_config(node),
        }

        catch_config = self._build_catch_config(node, graph)
        if catch_config:
            state["Catch"] = catch_config

        next_state = self._find_next_state(node, graph, EdgeTrigger.SUCCESS)
        if next_state:
            state["Next"] = next_state
        else:
            state["End"] = True

        return state

    def _create_pass_state(self, node) -> dict:
        """Fallback: Pass state for unsupported node types."""
        return {
            "Type": "Pass",
            "Comment": f"Placeholder for {node.kind} node",
            "End": True,
        }

    def _build_lambda_arn(self, function_name: str) -> str:
        """Construct Lambda ARN from function name."""
        return f"arn:aws:lambda:{self.region}:{self.account_id}:function:{self.lambda_prefix}-{function_name}"

    def _build_retry_config(self, node) -> list:
        """
        Build retry configuration from node policy.

        Production pattern: Exponential backoff with jitter.
        """
        retry_policy = getattr(node, "retry", None)

        if not retry_policy:
            return [
                {
                    "ErrorEquals": [
                        "States.TaskFailed",
                        "States.Timeout",
                        "Lambda.ServiceException",
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 3,
                    "BackoffRate": 2.0,
                    "JitterStrategy": "FULL",
                }
            ]

        strategy = getattr(retry_policy, "strategy", None)
        backoff_rate = 2.0 if strategy and strategy.value == "exponential" else 1.0

        return [
            {
                "ErrorEquals": ["States.ALL"],
                "IntervalSeconds": int(getattr(retry_policy, "backoff_seconds", 2)),
                "MaxAttempts": getattr(retry_policy, "max_attempts", 3),
                "BackoffRate": backoff_rate,
            }
        ]

    def _build_catch_config(self, node, graph: GraphSpec) -> list:
        """Build error handling (Catch) from edges with error trigger."""
        error_edges = [
            e
            for e in graph.edges
            if e.from_node == node.id
            and e.condition
            and e.condition.trigger == EdgeTrigger.ERROR
        ]

        if not error_edges:
            return []

        catches = []
        for edge in error_edges:
            catches.append({
                "ErrorEquals": ["States.ALL"],
                "Next": edge.to_node,
                "ResultPath": "$.error",
            })

        return catches

    def _find_next_state(
        self, node, graph: GraphSpec, trigger: EdgeTrigger
    ) -> Optional[str]:
        """Find next state for a given trigger type."""
        for edge in graph.edges:
            if edge.from_node == node.id:
                if edge.condition and edge.condition.trigger == trigger:
                    return edge.to_node
                elif not edge.condition and trigger == EdgeTrigger.SUCCESS:
                    return edge.to_node
        return None

    def _get_graph_timeout(self, graph: GraphSpec) -> int:
        """Get graph-level timeout in seconds (default: 1 hour)."""
        timeout = getattr(graph, "timeout", None)
        if timeout and hasattr(timeout, "seconds"):
            return int(timeout.seconds)
        return 3600

    def to_json(self, asl: dict, indent: int = 2) -> str:
        """Convert ASL dict to formatted JSON string."""
        return json.dumps(asl, indent=indent)

    def save(self, asl: dict, filepath: str) -> None:
        """Save ASL to JSON file."""
        with open(filepath, "w") as f:
            json.dump(asl, f, indent=2)
        logger.info("[OK] Saved ASL to %s", filepath)

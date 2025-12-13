"""
Generator interface for all backends.

All generators (LangGraph, AWS, MCP, YAML) implement this interface.
Generators convert ManifestIR → target format.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol, runtime_checkable

import yaml

from . import (
    EdgeTrigger,
    GraphIR,
    ManifestIR,
    NodeIR,
    NodeKind,
)

logger = logging.getLogger(__name__)


@runtime_checkable
class Generator(Protocol):
    """
    Protocol for all generators (backends).

    Generators convert ManifestIR → target format.
    """

    def generate(self, ir: ManifestIR) -> str:
        """
        Generate target format from IR.

        Args:
            ir: ManifestIR

        Returns:
            Generated code/config as string
        """
        ...


class LangGraphGenerator:
    """Generate LangGraph Python code from ManifestIR."""

    def generate(self, ir: ManifestIR) -> str:
        """Generate LangGraph Python code."""
        lines = [
            '"""',
            f"Auto-generated LangGraph agent: {ir.name}",
            f"{ir.description}",
            '"""',
            "",
            "from langgraph.graph import StateGraph, START, END",
            "from typing import TypedDict, Any",
            "",
            "",
            "class State(TypedDict):",
            '    """Agent state."""',
            "    context: dict",
            "    history: list[dict]",
            "    current_node: str",
            "",
            "",
        ]

        graph = ir.graphs[0] if ir.graphs else None
        if not graph:
            return "\n".join(lines) + "# No graphs defined\n"

        # Generate stub functions for each node
        for node in graph.nodes:
            lines.extend(
                [
                    f"def {node.id}_function(state: State) -> State:",
                    f'    """',
                    f"    {node.label}",
                    f"    {node.description or 'No description'}",
                    f'    """',
                    f'    state["current_node"] = "{node.id}"',
                    "    # TODO: Implement node logic",
                    "    return state",
                    "",
                    "",
                ]
            )

        # Generate router functions
        for router in ir.routers:
            # Find edges from router node
            router_node = None
            for node in graph.nodes:
                if node.router_ref == router.name:
                    router_node = node
                    break

            if router_node:
                routes = []
                for edge in graph.edges:
                    if edge.from_node == router_node.id and edge.condition.route:
                        routes.append(edge.condition.route)

                lines.extend(
                    [
                        f"def {router.name}(state: State) -> str:",
                        f'    """',
                        f"    Router: {router.name}",
                        f"    Strategy: {router.strategy.value}",
                        f'    """',
                        "    # TODO: Implement routing logic",
                        f'    return "{routes[0] if routes else "default"}"',
                        "",
                        "",
                    ]
                )

        # Build graph
        lines.extend(
            [
                "# Build graph",
                "graph = StateGraph(State)",
                "",
            ]
        )

        # Add nodes
        for node in graph.nodes:
            lines.append(f'graph.add_node("{node.id}", {node.id}_function)')
        lines.append("")

        # Add edges
        lines.append(f"# Entry point")
        lines.append(f'graph.add_edge(START, "{graph.entry_node}")')
        lines.append("")

        # Group edges by source for conditional edges
        edges_by_source: Dict[str, List] = {}
        for edge in graph.edges:
            if edge.from_node not in edges_by_source:
                edges_by_source[edge.from_node] = []
            edges_by_source[edge.from_node].append(edge)

        for from_node, edges in edges_by_source.items():
            node = graph.get_node(from_node)

            if node and node.kind == NodeKind.ROUTER and node.router_ref:
                # Conditional edges
                path_map = {}
                for edge in edges:
                    if edge.condition.route:
                        path_map[edge.condition.route] = edge.to_node
                    else:
                        path_map["default"] = edge.to_node

                lines.append(f"graph.add_conditional_edges(")
                lines.append(f'    "{from_node}",')
                lines.append(f"    {node.router_ref},")
                lines.append(f"    {path_map},")
                lines.append(f")")
            else:
                # Simple edges
                for edge in edges:
                    to_node = edge.to_node
                    lines.append(f'graph.add_edge("{from_node}", "{to_node}")')

        lines.append("")

        # Find terminal nodes (no outgoing edges)
        terminal_nodes = [
            n.id for n in graph.nodes if not graph.get_outgoing_edges(n.id)
        ]
        for terminal in terminal_nodes:
            lines.append(f'graph.add_edge("{terminal}", END)')

        lines.extend(
            [
                "",
                "# Compile",
                "compiled = graph.compile()",
                "",
                "",
                'if __name__ == "__main__":',
                "    # Test execution",
                '    result = compiled.invoke({"context": {}, "history": [], "current_node": ""})',
                "    print(result)",
            ]
        )

        return "\n".join(lines)


class AWSGenerator:
    """Generate AWS Step Functions ASL from ManifestIR."""

    def __init__(self, lambda_arn_prefix: str = "arn:aws:lambda:::function:uaa"):
        self.lambda_arn_prefix = lambda_arn_prefix

    def generate(self, ir: ManifestIR) -> str:
        """Generate ASL JSON."""
        graph = ir.graphs[0] if ir.graphs else None
        if not graph:
            return json.dumps({"Comment": "Empty", "States": {}}, indent=2)

        asl = {
            "Comment": ir.description or f"Agent: {ir.name}",
            "StartAt": graph.entry_node,
            "States": {},
        }

        for node in graph.nodes:
            asl["States"][node.id] = self._generate_state(node, graph, ir)

        return json.dumps(asl, indent=2)

    def _generate_state(
        self, node: NodeIR, graph: GraphIR, manifest: ManifestIR
    ) -> Dict[str, Any]:
        """Generate ASL state from NodeIR."""
        outgoing = graph.get_outgoing_edges(node.id)

        if node.kind == NodeKind.ROUTER:
            return self._generate_choice_state(node, outgoing)
        else:
            return self._generate_task_state(node, outgoing)

    def _generate_task_state(self, node: NodeIR, edges: List) -> Dict[str, Any]:
        """Generate Task state."""
        state: Dict[str, Any] = {
            "Type": "Task",
            "Resource": f"{self.lambda_arn_prefix}-{node.id}",
            "Retry": [
                {
                    "ErrorEquals": ["States.TaskFailed", "States.Timeout"],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 3,
                    "BackoffRate": 2.0,
                    "JitterStrategy": "FULL",
                }
            ],
        }

        if node.description:
            state["Comment"] = node.description

        # Add next state or end
        success_edges = [e for e in edges if e.condition.trigger == EdgeTrigger.SUCCESS]
        error_edges = [e for e in edges if e.condition.trigger == EdgeTrigger.ERROR]

        if success_edges:
            state["Next"] = success_edges[0].to_node
        else:
            state["End"] = True

        # Add Catch for error handling
        if error_edges:
            state["Catch"] = [
                {
                    "ErrorEquals": ["States.ALL"],
                    "Next": error_edges[0].to_node,
                }
            ]

        return state

    def _generate_choice_state(self, node: NodeIR, edges: List) -> Dict[str, Any]:
        """Generate Choice state for router."""
        state: Dict[str, Any] = {
            "Type": "Choice",
            "Choices": [],
        }

        if node.description:
            state["Comment"] = node.description

        default_target = None

        for edge in edges:
            if edge.condition.route:
                choice = {
                    "Variable": "$.route",
                    "StringEquals": edge.condition.route,
                    "Next": edge.to_node,
                }
                state["Choices"].append(choice)
            elif edge.condition.trigger == EdgeTrigger.ALWAYS:
                default_target = edge.to_node

        if default_target:
            state["Default"] = default_target
        elif edges:
            state["Default"] = edges[0].to_node

        return state


class YAMLGenerator:
    """Generate UAA YAML from ManifestIR."""

    def generate(self, ir: ManifestIR) -> str:
        """Generate UAA YAML."""
        data = {
            "name": ir.name,
            "version": ir.version,
            "description": ir.description,
            "graphs": [self._generate_graph(g) for g in ir.graphs],
            "tools": [self._generate_tool(t) for t in ir.tools],
            "routers": [self._generate_router(r) for r in ir.routers],
        }

        if ir.policies:
            data["policies"] = ir.policies

        return yaml.dump(data, sort_keys=False, default_flow_style=False)

    def _generate_graph(self, graph: GraphIR) -> Dict:
        """Generate graph dict."""
        return {
            "name": graph.name,
            "entry_node": graph.entry_node,
            "nodes": [
                {
                    "id": n.id,
                    "kind": n.kind.value,
                    "label": n.label,
                    **({"description": n.description} if n.description else {}),
                    **(
                        {"router": {"name": n.router_ref}}
                        if n.router_ref
                        else {}
                    ),
                    **({"tool": {"name": n.tool_ref}} if n.tool_ref else {}),
                }
                for n in graph.nodes
            ],
            "edges": [
                {
                    "from_node": e.from_node,
                    "to_node": e.to_node,
                    "condition": {
                        "trigger": e.condition.trigger.value,
                        **(
                            {"expression": e.condition.expression}
                            if e.condition.expression
                            else {}
                        ),
                        **({"route": e.condition.route} if e.condition.route else {}),
                    },
                }
                for e in graph.edges
            ],
        }

    def _generate_tool(self, tool) -> Dict:
        """Generate tool dict."""
        return {
            "name": tool.name,
            "description": tool.description,
            "protocol": tool.protocol,
            **({"config": tool.config} if tool.config else {}),
        }

    def _generate_router(self, router) -> Dict:
        """Generate router dict."""
        return {
            "name": router.name,
            "strategy": router.strategy.value,
            **(
                {"system_message": router.system_message}
                if router.system_message
                else {}
            ),
            **(
                {"model_candidates": router.model_candidates}
                if router.model_candidates
                else {}
            ),
            **({"default_model": router.default_model} if router.default_model else {}),
        }


# Generator registry - kept for backwards compatibility
# New code should use generator_registry module directly
GENERATORS: Dict[str, Generator] = {
    "langgraph": LangGraphGenerator(),
    "aws": AWSGenerator(),
    "yaml": YAMLGenerator(),
    "uaa": YAMLGenerator(),  # Alias
}


def get_generator(target_type: str) -> Generator:
    """
    Get generator by target type.
    
    DEPRECATED: Use universal_agent_nexus.generator_registry.get_generator() instead.
    This function is kept for backwards compatibility.
    """
    # Try to use registry if available (avoid circular import)
    try:
        from universal_agent_nexus.generator_registry import get_generator as get_from_registry
        return get_from_registry(target_type)
    except (ImportError, ValueError):
        # Fallback to old behavior
        if target_type not in GENERATORS:
            raise ValueError(f"Unknown target type: {target_type}")
        return GENERATORS[target_type]


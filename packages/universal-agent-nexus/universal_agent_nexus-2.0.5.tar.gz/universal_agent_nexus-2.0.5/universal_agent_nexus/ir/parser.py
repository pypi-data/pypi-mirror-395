"""
Parser interface for all frontends.

All parsers (LangGraph, AWS, MCP, YAML) implement this interface.
Parsers convert source formats → ManifestIR.
"""

import ast
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

import yaml

from . import (
    EdgeCondition,
    EdgeIR,
    EdgeTrigger,
    GraphIR,
    ManifestIR,
    Metadata,
    NodeIR,
    NodeKind,
    RouterIR,
    RouterStrategy,
    SourceLocation,
    ToolIR,
)

logger = logging.getLogger(__name__)


@runtime_checkable
class Parser(Protocol):
    """
    Protocol for all parsers (frontends).

    Parsers convert source formats → ManifestIR.
    """

    def parse(self, source: str) -> ManifestIR:
        """
        Parse source and produce IR.

        Args:
            source: Path to source file or source string

        Returns:
            ManifestIR
        """
        ...

    def can_parse(self, source: str) -> bool:
        """
        Check if this parser can handle the source.

        Args:
            source: Path to source file or source string

        Returns:
            True if parser can handle this source
        """
        ...


class LangGraphParser:
    """
    Parse LangGraph Python → ManifestIR.

    Uses stdlib ast for fast parsing (libCST available for lossless mode).
    """

    def parse(self, source: str) -> ManifestIR:
        """Parse LangGraph code using stdlib ast."""
        path = Path(source)

        if path.exists():
            code = path.read_text(encoding="utf-8")
            source_name = str(path)
        else:
            code = source
            source_name = "<string>"

        tree = ast.parse(code)
        extractor = _LangGraphExtractor(source_name)
        extractor.visit(tree)

        # Validate
        if not extractor.nodes:
            raise ValueError(f"No StateGraph nodes found in {source_name}")

        entry_node = extractor.entry_node or extractor.nodes[0].id
        logger.info(
            f"Parsed LangGraph: {len(extractor.nodes)} nodes, {len(extractor.edges)} edges"
        )

        return ManifestIR(
            name=self._sanitize_name(source_name),
            version="1.0.0",
            description=f"Parsed from LangGraph: {Path(source_name).name}",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node=entry_node,
                    nodes=extractor.nodes,
                    edges=extractor.edges,
                )
            ],
            tools=extractor.tools,
            routers=extractor.routers,
            metadata=Metadata({"source": source_name, "parser": "langgraph"}),
        )

    def can_parse(self, source: str) -> bool:
        """Check if source is LangGraph Python code."""
        path = Path(source)

        if path.exists():
            if not source.endswith(".py"):
                return False
            try:
                content = path.read_text()
                return "StateGraph" in content or "langgraph" in content.lower()
            except Exception:
                return False
        else:
            # String source
            return "StateGraph" in source or "add_node" in source

    def _sanitize_name(self, source_name: str) -> str:
        """Convert file path to valid manifest name."""
        name = Path(source_name).stem
        name = name.replace("_", "-").lower()
        name = "".join(c for c in name if c.isalnum() or c == "-")
        return name or "langgraph-agent"


class _LangGraphExtractor(ast.NodeVisitor):
    """AST visitor to extract StateGraph structure."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.nodes: List[NodeIR] = []
        self.edges: List[EdgeIR] = []
        self.tools: List[ToolIR] = []
        self.routers: List[RouterIR] = []
        self.entry_node: Optional[str] = None
        self._seen_nodes: set = set()

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls to extract StateGraph methods."""
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr

            if method == "add_node":
                self._extract_node(node)
            elif method == "add_edge":
                self._extract_edge(node)
            elif method == "add_conditional_edges":
                self._extract_conditional_edge(node)
            elif method == "set_entry_point":
                self._extract_entry_point(node)

        self.generic_visit(node)

    def _extract_node(self, node: ast.Call):
        """Extract node from add_node call."""
        if not node.args:
            return

        node_id = self._get_string_value(node.args[0])
        if not node_id or node_id in self._seen_nodes:
            return

        self._seen_nodes.add(node_id)

        fn_name = ""
        if len(node.args) >= 2:
            fn_name = self._get_name(node.args[1])

        kind = self._infer_kind(fn_name)

        self.nodes.append(
            NodeIR(
                id=node_id,
                kind=kind,
                label=node_id.replace("_", " ").title(),
                description=f"Function: {fn_name}" if fn_name else None,
                source_location=SourceLocation(
                    file=self.source_name,
                    line=node.lineno,
                    column=node.col_offset,
                ),
            )
        )

    def _extract_edge(self, node: ast.Call):
        """Extract edge from add_edge call."""
        if len(node.args) < 2:
            return

        from_node = self._get_string_value(node.args[0])
        to_node = self._get_string_value(node.args[1])

        # Skip START/END constants
        if self._is_constant(node.args[0]) and from_node.upper() in (
            "START",
            "__START__",
        ):
            return
        if self._is_constant(node.args[1]) and to_node.upper() in ("END", "__END__"):
            return

        if from_node and to_node:
            self.edges.append(
                EdgeIR(
                    from_node=from_node,
                    to_node=to_node,
                    condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                )
            )

    def _extract_conditional_edge(self, node: ast.Call):
        """Extract conditional edge with router."""
        if not node.args:
            return

        from_node = self._get_string_value(node.args[0])
        if not from_node:
            return

        router_fn = ""
        if len(node.args) >= 2:
            router_fn = self._get_name(node.args[1])

        path_map = {}
        if len(node.args) >= 3 and isinstance(node.args[2], ast.Dict):
            for key, value in zip(node.args[2].keys, node.args[2].values):
                k = self._get_string_value(key) if key else None
                v = self._get_string_value(value)
                if k and v:
                    path_map[k] = v

        # Create router
        router_name = f"{from_node}_router"
        self.routers.append(
            RouterIR(
                name=router_name,
                strategy=RouterStrategy.LLM,
                model_candidates=["gpt-4o-mini"],
                default_model="gpt-4o-mini",
                metadata=Metadata({"function": router_fn} if router_fn else {}),
            )
        )

        # Update node to router kind
        for n in self.nodes:
            if n.id == from_node:
                n.kind = NodeKind.ROUTER
                n.router_ref = router_name
                break

        # Add conditional edges
        for route_key, target in path_map.items():
            if target.upper() not in ("END", "__END__"):
                self.edges.append(
                    EdgeIR(
                        from_node=from_node,
                        to_node=target,
                        condition=EdgeCondition(
                            trigger=EdgeTrigger.SUCCESS, route=route_key
                        ),
                    )
                )

    def _extract_entry_point(self, node: ast.Call):
        """Extract entry point."""
        if node.args:
            entry = self._get_string_value(node.args[0])
            if entry and not (
                self._is_constant(node.args[0])
                and entry.upper() in ("START", "__START__")
            ):
                self.entry_node = entry

    def _get_string_value(self, node: ast.expr) -> str:
        """Extract string value from AST node."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def _get_name(self, node: ast.expr) -> str:
        """Get function/variable name."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def _is_constant(self, node: ast.expr) -> bool:
        """Check if node is a Name constant (not string literal)."""
        return isinstance(node, ast.Name)

    def _infer_kind(self, fn_name: str) -> NodeKind:
        """Infer node kind from function name."""
        fn_lower = fn_name.lower()
        if any(kw in fn_lower for kw in ["router", "route", "routing", "decide"]):
            return NodeKind.ROUTER
        elif any(kw in fn_lower for kw in ["tool", "call_", "invoke_"]):
            return NodeKind.TOOL
        return NodeKind.TASK


class AWSParser:
    """Parse AWS Step Functions ASL → ManifestIR."""

    def parse(self, source: str) -> ManifestIR:
        """Parse ASL JSON."""
        path = Path(source)

        if path.exists():
            with open(path) as f:
                asl = json.load(f)
            source_name = str(path)
        else:
            asl = json.loads(source)
            source_name = "<string>"

        states = asl.get("States", {})
        start_at = asl.get("StartAt")

        nodes = []
        edges = []
        tools = []

        for state_name, state_def in states.items():
            node = self._convert_state(state_name, state_def)
            nodes.append(node)
            edges.extend(self._extract_edges(state_name, state_def))

            # Extract Lambda tool
            if state_def.get("Type") == "Task":
                resource = state_def.get("Resource", "")
                if "lambda" in resource.lower():
                    tools.append(
                        ToolIR(
                            name=state_name,
                            description=f"Lambda: {resource}",
                            protocol="aws_lambda",
                            config={"resource": resource},
                        )
                    )

        logger.info(f"Parsed ASL: {len(nodes)} states, {len(edges)} transitions")

        return ManifestIR(
            name=self._sanitize_name(asl.get("Comment", source_name)),
            version="1.0.0",
            description=asl.get("Comment", f"Imported from AWS: {source_name}"),
            graphs=[
                GraphIR(
                    name="main",
                    entry_node=start_at,
                    nodes=nodes,
                    edges=edges,
                )
            ],
            tools=tools,
            metadata=Metadata({"source": source_name, "parser": "aws"}),
        )

    def can_parse(self, source: str) -> bool:
        """Check if source is ASL JSON."""
        path = Path(source)

        if path.exists():
            if not source.endswith(".json"):
                return False
            try:
                with open(path) as f:
                    data = json.load(f)
                return "States" in data and "StartAt" in data
            except Exception:
                return False
        else:
            try:
                data = json.loads(source)
                return "States" in data and "StartAt" in data
            except Exception:
                return False

    def _convert_state(self, name: str, state: Dict) -> NodeIR:
        """Convert ASL state to NodeIR."""
        state_type = state.get("Type", "Task")

        if state_type == "Choice":
            kind = NodeKind.ROUTER
        elif state_type == "Task":
            kind = NodeKind.TASK
        else:
            kind = NodeKind.TASK

        return NodeIR(
            id=name,
            kind=kind,
            label=name.replace("_", " ").title(),
            description=state.get("Comment"),
            config={"aws_type": state_type},
        )

    def _extract_edges(self, state_name: str, state: Dict) -> List[EdgeIR]:
        """Extract edges from ASL state."""
        edges = []
        state_type = state.get("Type", "Task")

        if state_type == "Choice":
            for choice in state.get("Choices", []):
                if "Next" in choice:
                    edges.append(
                        EdgeIR(
                            from_node=state_name,
                            to_node=choice["Next"],
                            condition=EdgeCondition(
                                trigger=EdgeTrigger.SUCCESS,
                                expression=self._choice_to_expr(choice),
                            ),
                        )
                    )
            if "Default" in state:
                edges.append(
                    EdgeIR(
                        from_node=state_name,
                        to_node=state["Default"],
                        condition=EdgeCondition(trigger=EdgeTrigger.ALWAYS),
                    )
                )
        elif "Next" in state:
            edges.append(
                EdgeIR(
                    from_node=state_name,
                    to_node=state["Next"],
                    condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                )
            )

        # Error handling (Catch)
        for catch in state.get("Catch", []):
            if "Next" in catch:
                edges.append(
                    EdgeIR(
                        from_node=state_name,
                        to_node=catch["Next"],
                        condition=EdgeCondition(trigger=EdgeTrigger.ERROR),
                    )
                )

        return edges

    def _choice_to_expr(self, choice: Dict) -> str:
        """Convert ASL Choice to expression."""
        if "StringEquals" in choice:
            var = choice.get("Variable", "$.value")
            return f'{var} == "{choice["StringEquals"]}"'
        elif "NumericEquals" in choice:
            var = choice.get("Variable", "$.value")
            return f"{var} == {choice['NumericEquals']}"
        elif "BooleanEquals" in choice:
            var = choice.get("Variable", "$.value")
            return f"{var} == {choice['BooleanEquals']}"
        return "True"

    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for manifest."""
        name = name.lower().replace(" ", "-")
        return "".join(c for c in name if c.isalnum() or c == "-") or "aws-agent"


class YAMLParser:
    """Parse UAA YAML → ManifestIR."""

    @staticmethod
    def _get_ref_value(node_dict: dict, key: str) -> Optional[str]:
        """
        Support both nested and flat formats for refs.
        
        Nested format: router: {name: "router_name"}
        Flat format: router_ref: "router_name"
        """
        # Try nested format first: router: {name: "..."}
        if key in node_dict and isinstance(node_dict[key], dict):
            return node_dict[key].get("name")
        
        # Fall back to flat format: router_ref: "..."
        if f"{key}_ref" in node_dict:
            return node_dict[f"{key}_ref"]
        
        return None

    def parse(self, source: str) -> ManifestIR:
        """Parse UAA YAML."""
        path = Path(source)

        # Check if source is a file path (handling OSError for long strings)
        is_file = False
        try:
            is_file = path.exists()
        except OSError:
            # String too long to be a path - treat as YAML content
            pass

        if is_file:
            with open(path) as f:
                data = yaml.safe_load(f)
            source_name = str(path)
        else:
            data = yaml.safe_load(source)
            source_name = "<string>"

        graphs = []
        for g in data.get("graphs", []):
            nodes = [
                NodeIR(
                    id=n["id"],
                    kind=NodeKind(n.get("kind", "task")),
                    label=n.get("label", n["id"]),
                    description=n.get("description"),
                    router_ref=self._get_ref_value(n, "router"),
                    tool_ref=self._get_ref_value(n, "tool"),
                )
                for n in g.get("nodes", [])
            ]

            edges = [
                EdgeIR(
                    from_node=e["from_node"],
                    to_node=e["to_node"],
                    condition=EdgeCondition(
                        trigger=EdgeTrigger(
                            e.get("condition", {}).get("trigger", "success")
                        ),
                        expression=e.get("condition", {}).get("expression"),
                        route=e.get("condition", {}).get("route"),
                    ),
                )
                for e in g.get("edges", [])
            ]

            graphs.append(
                GraphIR(
                    name=g.get("name", "main"),
                    entry_node=g.get("entry_node"),
                    nodes=nodes,
                    edges=edges,
                )
            )

        tools = [
            ToolIR(
                name=t["name"],
                description=t.get("description", ""),
                protocol=t.get("protocol", "mcp"),
                config=t.get("config", {}),
            )
            for t in data.get("tools", [])
        ]

        routers = [
            RouterIR(
                name=r["name"],
                strategy=RouterStrategy(r.get("strategy", "llm")),
                system_message=r.get("system_message"),
                model_candidates=r.get("model_candidates", []),
                default_model=r.get("default_model"),
            )
            for r in data.get("routers", [])
        ]

        return ManifestIR(
            name=data.get("name", "uaa-agent"),
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            graphs=graphs,
            tools=tools,
            routers=routers,
            policies=data.get("policies", []),
            metadata=Metadata({"source": source_name, "parser": "yaml"}),
        )

    def can_parse(self, source: str) -> bool:
        """Check if source is UAA YAML."""
        path = Path(source)

        if path.exists():
            return source.endswith((".yaml", ".yml"))
        else:
            try:
                data = yaml.safe_load(source)
                return isinstance(data, dict) and "graphs" in data
            except Exception:
                return False


# Parser registry - kept for backwards compatibility
# New code should use parser_registry module directly
PARSERS: Dict[str, Parser] = {
    "langgraph": LangGraphParser(),
    "aws": AWSParser(),
    "yaml": YAMLParser(),
    "uaa": YAMLParser(),  # Alias
}


def get_parser(source_type: str) -> Parser:
    """
    Get parser by source type.
    
    DEPRECATED: Use universal_agent_nexus.parser_registry.get_parser() instead.
    This function is kept for backwards compatibility.
    """
    if source_type not in PARSERS:
        raise ValueError(f"Unknown source type: {source_type}")
    return PARSERS[source_type]


def detect_source_type(source: str) -> str:
    """
    Auto-detect source type.
    
    DEPRECATED: Use universal_agent_nexus.parser_registry.detect_source_type() instead.
    This function is kept for backwards compatibility.
    """
    # Try to use registry if available (avoid circular import)
    try:
        from universal_agent_nexus.parser_registry import detect_source_type as detect_from_registry
        return detect_from_registry(source)
    except (ImportError, ValueError):
        # Fallback to old behavior
        for source_type, parser in PARSERS.items():
            if source_type == "uaa":
                continue  # Skip alias
            if parser.can_parse(source):
                return source_type
        raise ValueError(f"Cannot detect source type for: {source}")


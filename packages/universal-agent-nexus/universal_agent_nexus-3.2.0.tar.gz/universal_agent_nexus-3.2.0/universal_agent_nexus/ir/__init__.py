"""
Universal Agent Intermediate Representation.

The IR is the CORE ABSTRACTION that enables:
- Bidirectional translation (any source ↔ any target)
- Transformation passes (optimizations, validations)
- Multiple frontends (parsers) and backends (generators)
- Future extensibility without breaking existing code

Architecture:
    Parser → IR → Transformer → Generator

Example:
    LangGraph → GraphIR → optimize() → AWS ASL
    AWS ASL → GraphIR → optimize() → LangGraph
    MCP → GraphIR → optimize() → YAML → Fabric
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Type, TypeVar
from enum import Enum
import logging

# Safe expression evaluation - no eval() RCE vulnerability
from simpleeval import SimpleEval, NameNotDefined

T = TypeVar('T')
logger = logging.getLogger(__name__)


# ===== ENUMS =====


class NodeKind(str, Enum):
    """Node type in agent graph."""

    TASK = "task"
    ROUTER = "router"
    TOOL = "tool"


class EdgeTrigger(str, Enum):
    """Edge trigger condition."""

    SUCCESS = "success"
    ERROR = "error"
    ALWAYS = "always"


class RouterStrategy(str, Enum):
    """Router decision strategy."""

    LLM = "llm"
    FUNCTION = "function"
    SWITCH = "switch"


# ===== CORE IR STRUCTURES =====


@dataclass
class SourceLocation:
    """Source code location for debugging/tracing."""

    file: str
    line: int
    column: int = 0

    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}"


@dataclass
class Metadata:
    """
    Enhanced metadata with annotation support.

    Supports both generic key-value data and typed annotations.
    """

    data: Dict[str, Any] = field(default_factory=dict)
    _annotations: Dict[str, Any] = field(default_factory=dict, repr=False)

    def get(self, key: str, default: Any = None) -> Any:
        """Get generic metadata value."""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set generic metadata value."""
        self.data[key] = value

    def update(self, other: Dict[str, Any]) -> None:
        """Update generic metadata from dict."""
        self.data.update(other)

    def annotate(self, annotation) -> None:
        """
        Add typed annotation.

        Args:
            annotation: Annotation instance (must implement Annotation interface)

        Example:
            from universal_agent_nexus.ir.annotations import CostAnnotation
            node.metadata.annotate(CostAnnotation(tokens=500, latency_ms=250, cost_cents=0.05))
        """
        from .annotations import Annotation
        if not isinstance(annotation, Annotation):
            raise TypeError(f"Annotation must implement Annotation interface, got {type(annotation)}")
        self._annotations[annotation.key()] = annotation

    def get_annotation(self, annotation_type: Type[T]) -> Optional[T]:
        """
        Get annotation by type.

        Args:
            annotation_type: Annotation class (e.g., CostAnnotation)

        Returns:
            Annotation instance or None if not found

        Example:
            cost = node.metadata.get_annotation(CostAnnotation)
            if cost:
                print(f"Est. cost: ${cost.cost_cents/100}")
        """
        from .annotations import Annotation
        if not issubclass(annotation_type, Annotation):
            raise TypeError(f"annotation_type must be an Annotation subclass, got {annotation_type}")
        key = annotation_type.key()
        return self._annotations.get(key)

    def list_annotations(self) -> Dict[str, Any]:
        """
        List all annotations.

        Returns:
            Dict mapping annotation keys to annotation instances
        """
        return self._annotations.copy()

    def has_annotation(self, annotation_type: Type[T]) -> bool:
        """
        Check if annotation exists.

        Args:
            annotation_type: Annotation class

        Returns:
            True if annotation exists
        """
        from .annotations import Annotation
        if not issubclass(annotation_type, Annotation):
            raise TypeError(f"annotation_type must be an Annotation subclass, got {annotation_type}")
        key = annotation_type.key()
        return key in self._annotations


@dataclass
class NodeIR:
    """
    Universal node representation.

    Represents a single step in agent execution:
    - Task nodes: Execute business logic
    - Router nodes: Make branching decisions
    - Tool nodes: Call external APIs/tools
    """

    id: str
    kind: NodeKind
    label: str
    description: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    source_location: Optional[SourceLocation] = None
    metadata: Metadata = field(default_factory=Metadata)

    # Kind-specific fields
    router_ref: Optional[str] = None  # For router nodes
    tool_ref: Optional[str] = None  # For tool nodes


@dataclass
class EdgeCondition:
    """Edge transition condition."""

    trigger: EdgeTrigger = EdgeTrigger.SUCCESS
    expression: Optional[str] = None  # Python expression
    route: Optional[str] = None  # Router route key

    def evaluate(self, context: Dict[str, Any]) -> bool:
        """
        Evaluate condition against context using safe expression evaluation.
        
        Uses simpleeval to prevent RCE vulnerabilities from malicious expressions.
        """
        if self.trigger == EdgeTrigger.ALWAYS:
            return True

        if self.expression:
            evaluator = SimpleEval(
                names=context,
                functions={
                    "len": len,
                    "min": min,
                    "max": max,
                    "str": str,
                    "int": int,
                    "float": float,
                    "bool": bool,
                    "abs": abs,
                }
            )
            try:
                return bool(evaluator.eval(self.expression))
            except NameNotDefined as e:
                logger.debug("Expression '%s' has undefined name: %s", self.expression, e)
                return False
            except Exception as e:
                logger.debug("Expression '%s' evaluation failed: %s", self.expression, e)
                return False

        return True


@dataclass
class EdgeIR:
    """
    Universal edge representation.

    Represents a transition between nodes with optional conditions.
    """

    from_node: str
    to_node: str
    condition: EdgeCondition = field(default_factory=EdgeCondition)
    metadata: Metadata = field(default_factory=Metadata)


@dataclass
class RouterIR:
    """
    Router definition (decision logic).

    Routers determine which path to take from a router node.
    """

    name: str
    strategy: RouterStrategy = RouterStrategy.LLM
    system_message: Optional[str] = None
    model_candidates: List[str] = field(default_factory=list)
    default_model: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Metadata = field(default_factory=Metadata)


@dataclass
class ToolIR:
    """
    Tool definition (external capability).

    Tools represent external APIs, functions, or services.
    """

    name: str
    description: str
    protocol: str = "mcp"  # mcp, http, subprocess, aws_lambda
    config: Dict[str, Any] = field(default_factory=dict)
    input_schema: Optional[Dict] = None
    output_schema: Optional[Dict] = None
    metadata: Metadata = field(default_factory=Metadata)


@dataclass
class GraphIR:
    """
    Universal graph representation.

    This is the CORE IR - all parsers produce this, all generators consume this.
    """

    name: str
    entry_node: str
    nodes: List[NodeIR] = field(default_factory=list)
    edges: List[EdgeIR] = field(default_factory=list)
    metadata: Metadata = field(default_factory=Metadata)

    def __post_init__(self):
        """Build indexes after initialization."""
        self._build_indexes()

    def _build_indexes(self):
        """Build lookup indexes for fast access."""
        self._node_index: Dict[str, NodeIR] = {node.id: node for node in self.nodes}
        self._edge_index: Dict[str, List[EdgeIR]] = {}
        for edge in self.edges:
            if edge.from_node not in self._edge_index:
                self._edge_index[edge.from_node] = []
            self._edge_index[edge.from_node].append(edge)

    def validate(self) -> List[str]:
        """
        Validate graph structure.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Build index if needed
        if not hasattr(self, "_node_index"):
            self._build_indexes()

        # Check entry node exists
        if self.entry_node not in self._node_index:
            errors.append(f"Entry node '{self.entry_node}' not found in nodes")

        # Check all edges reference valid nodes
        for edge in self.edges:
            if edge.from_node not in self._node_index:
                errors.append(f"Edge references unknown from_node: {edge.from_node}")
            if edge.to_node not in self._node_index:
                errors.append(f"Edge references unknown to_node: {edge.to_node}")

        # Check for duplicate node IDs
        node_ids = [n.id for n in self.nodes]
        duplicates = [x for x in node_ids if node_ids.count(x) > 1]
        if duplicates:
            errors.append(f"Duplicate node IDs: {set(duplicates)}")

        return errors

    def get_node(self, node_id: str) -> Optional[NodeIR]:
        """Get node by ID."""
        if not hasattr(self, "_node_index"):
            self._build_indexes()
        return self._node_index.get(node_id)

    def get_outgoing_edges(self, node_id: str) -> List[EdgeIR]:
        """Get all edges leaving a node."""
        if not hasattr(self, "_edge_index"):
            self._build_indexes()
        return self._edge_index.get(node_id, [])

    def get_incoming_edges(self, node_id: str) -> List[EdgeIR]:
        """Get all edges entering a node."""
        return [edge for edge in self.edges if edge.to_node == node_id]

    def find_unreachable_nodes(self) -> List[str]:
        """Find nodes that are never reached from entry point."""
        visited = set()
        stack = [self.entry_node]

        while stack:
            node_id = stack.pop()
            if node_id in visited:
                continue
            visited.add(node_id)

            for edge in self.get_outgoing_edges(node_id):
                stack.append(edge.to_node)

        return [node.id for node in self.nodes if node.id not in visited]

    def topological_sort(self) -> List[str]:
        """Return nodes in topological order (entry first)."""
        visited = set()
        order = []

        def dfs(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)
            for edge in self.get_outgoing_edges(node_id):
                dfs(edge.to_node)
            order.append(node_id)

        dfs(self.entry_node)
        return list(reversed(order))


@dataclass
class ManifestIR:
    """
    Complete agent manifest in IR form.

    Top-level container for entire agent definition.
    """

    name: str
    version: str
    description: str
    graphs: List[GraphIR] = field(default_factory=list)
    tools: List[ToolIR] = field(default_factory=list)
    routers: List[RouterIR] = field(default_factory=list)
    policies: List[Dict] = field(default_factory=list)
    metadata: Metadata = field(default_factory=Metadata)

    def __post_init__(self):
        """Build indexes after initialization."""
        self._build_indexes()

    def _build_indexes(self):
        """Build lookup indexes."""
        self._graph_index: Dict[str, GraphIR] = {g.name: g for g in self.graphs}
        self._tool_index: Dict[str, ToolIR] = {t.name: t for t in self.tools}
        self._router_index: Dict[str, RouterIR] = {r.name: r for r in self.routers}

    def get_graph(self, name: str) -> Optional[GraphIR]:
        """Get graph by name."""
        if not hasattr(self, "_graph_index"):
            self._build_indexes()
        return self._graph_index.get(name)

    def get_tool(self, name: str) -> Optional[ToolIR]:
        """Get tool by name."""
        if not hasattr(self, "_tool_index"):
            self._build_indexes()
        return self._tool_index.get(name)

    def get_router(self, name: str) -> Optional[RouterIR]:
        """Get router by name."""
        if not hasattr(self, "_router_index"):
            self._build_indexes()
        return self._router_index.get(name)

    def validate(self) -> List[str]:
        """
        Validate entire manifest.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        if not self.name:
            errors.append("Manifest name is required")
        if not self.graphs:
            errors.append("At least one graph is required")

        for graph in self.graphs:
            graph_errors = graph.validate()
            errors.extend([f"Graph '{graph.name}': {e}" for e in graph_errors])

        return errors


# ===== EXPORTS =====

__all__ = [
    # Enums
    "NodeKind",
    "EdgeTrigger",
    "RouterStrategy",
    # Core types
    "SourceLocation",
    "Metadata",
    "NodeIR",
    "EdgeCondition",
    "EdgeIR",
    "RouterIR",
    "ToolIR",
    "GraphIR",
    "ManifestIR",
]


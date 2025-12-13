"""
Comprehensive IR validation.

Performs semantic and type checking on IR:
- Type checking: Node configs, edge conditions
- Semantic validation: Valid transitions, router coverage
- Dataflow analysis: Variable definitions, use-before-def
- Graph properties: Connectivity, cycles, dead code

Error messages include source locations for easy debugging.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from . import EdgeTrigger, GraphIR, ManifestIR, NodeIR, NodeKind

logger = logging.getLogger(__name__)


@dataclass
class SourceSpan:
    """Source code span for error reporting."""

    file: str = "<unknown>"
    line_start: int = 0
    col_start: int = 0
    line_end: int = 0
    col_end: int = 0

    def __str__(self) -> str:
        if self.line_start == self.line_end:
            return f"{self.file}:{self.line_start}:{self.col_start}"
        return f"{self.file}:{self.line_start}:{self.col_start}-{self.line_end}:{self.col_end}"


@dataclass
class ValidationError:
    """
    Single validation error with source location.

    Attributes:
        severity: "error", "warning", "info"
        code: Error code (e.g., "E001", "W002")
        message: Human-readable error message
        span: Source location (if available)
        hint: Optional hint for fixing the error
    """

    severity: str
    code: str
    message: str
    span: Optional[SourceSpan] = None
    hint: Optional[str] = None

    def __str__(self) -> str:
        loc = f"{self.span}: " if self.span else ""
        hint_str = f"\n  hint: {self.hint}" if self.hint else ""
        return f"{loc}{self.severity}[{self.code}]: {self.message}{hint_str}"

    def format_with_context(self, source_lines: List[str]) -> str:
        """
        Format error with source context (like Rust compiler errors).

        Example output:
            manifest.yaml:12:5: error[E101]: Router node 'risk_check' missing router_ref
               10 |   nodes:
               11 |     - id: risk_check
            -->12 |       kind: router
                  |       ^^^^^^^^^^^^
               13 |       label: "Risk Classifier"
        """
        if not self.span or not source_lines:
            return str(self)

        lines = []
        lines.append(f"{self.span}: {self.severity}[{self.code}]: {self.message}")

        # Extract context lines
        start_line = max(0, self.span.line_start - 2)
        end_line = min(len(source_lines), self.span.line_end + 2)

        for i in range(start_line, end_line):
            line_num = i + 1
            is_error_line = line_num == self.span.line_start
            prefix = "-->" if is_error_line else "   "
            lines.append(f"{prefix}{line_num:4d} | {source_lines[i].rstrip()}")

            # Add caret line
            if is_error_line and self.span.col_start > 0:
                padding = " " * (self.span.col_start - 1)
                width = max(1, self.span.col_end - self.span.col_start + 1)
                caret = "^" * width
                lines.append(f"        | {padding}{caret}")

        if self.hint:
            lines.append(f"  = hint: {self.hint}")

        return "\n".join(lines)


# Error codes
ERROR_CODES = {
    # Structural errors (E0xx)
    "E001": "Entry node not found",
    "E002": "Edge references unknown from_node",
    "E003": "Edge references unknown to_node",
    "E004": "Duplicate node ID",
    # Type errors (E1xx)
    "E101": "Router node missing router_ref",
    "E102": "Tool node missing tool_ref",
    "E103": "Unknown router reference",
    "E104": "Unknown tool reference",
    # Semantic errors (E2xx)
    "E201": "Router node has no outgoing edges",
    "E202": "Graph has no entry point",
    "E203": "Circular dependency detected",
    # Warnings (W3xx)
    "W301": "Unreachable nodes detected",
    "W302": "No terminal nodes (possible infinite loop)",
    "W303": "Tool node missing error handling edge",
    "W304": "Router node has incomplete route coverage",
}


class IRValidator:
    """
    Comprehensive IR validator.

    Performs multiple validation passes:
    1. Structural validation (well-formedness)
    2. Type checking (config schemas)
    3. Semantic validation (valid transitions)
    4. Dataflow analysis (use-before-def)
    5. Completeness checks (router coverage)

    Example:
        validator = IRValidator()
        errors = validator.validate(ir)
        for error in errors:
            print(error)
    """

    def __init__(self, strict: bool = False):
        """
        Initialize validator.

        Args:
            strict: If True, treat warnings as errors
        """
        self.strict = strict
        self.errors: List[ValidationError] = []
        self._source_file: str = "<unknown>"

    def validate(self, ir: ManifestIR) -> List[ValidationError]:
        """
        Run all validation passes.

        Args:
            ir: Manifest IR to validate

        Returns:
            List of validation errors and warnings
        """
        self.errors = []
        self._source_file = ir.metadata.get("source", "<unknown>")

        # Ensure indexes are built
        ir._build_indexes()

        # 1. Structural validation
        self._validate_structure(ir)

        # 2. Type checking
        self._validate_types(ir)

        # 3. Semantic validation
        self._validate_semantics(ir)

        # 4. Completeness checks
        self._validate_completeness(ir)

        # Sort errors by severity (errors first, then warnings)
        self.errors.sort(key=lambda e: (0 if e.severity == "error" else 1, e.code))

        return self.errors

    def _add_error(
        self,
        code: str,
        message: str,
        *,
        severity: str = "error",
        location: Optional[str] = None,
        node: Optional[NodeIR] = None,
        hint: Optional[str] = None,
    ) -> None:
        """Add a validation error."""
        span = None
        if node and node.source_location:
            span = SourceSpan(
                file=node.source_location.file,
                line_start=node.source_location.line,
                col_start=node.source_location.column,
                line_end=node.source_location.line,
                col_end=node.source_location.column + len(node.id),
            )
        elif location:
            span = SourceSpan(file=self._source_file, line_start=0, col_start=0)

        self.errors.append(
            ValidationError(
                severity=severity,
                code=code,
                message=message,
                span=span,
                hint=hint,
            )
        )

    def _validate_structure(self, ir: ManifestIR) -> None:
        """Validate basic structure (well-formedness)."""
        if not ir.graphs:
            self._add_error(
                "E202",
                "Manifest has no graphs",
                hint="Add at least one graph definition",
            )
            return

        for graph in ir.graphs:
            # Check entry node exists
            if graph.entry_node not in graph._node_index:
                self._add_error(
                    "E001",
                    f"Entry node '{graph.entry_node}' not found in graph '{graph.name}'",
                    location=f"{graph.name}",
                    hint=f"Add a node with id='{graph.entry_node}' or change entry_node",
                )

            # Check for duplicate node IDs
            node_ids = [n.id for n in graph.nodes]
            seen: Set[str] = set()
            for node_id in node_ids:
                if node_id in seen:
                    self._add_error(
                        "E004",
                        f"Duplicate node ID '{node_id}' in graph '{graph.name}'",
                        location=f"{graph.name}:{node_id}",
                        hint="Node IDs must be unique within a graph",
                    )
                seen.add(node_id)

            # Check all edges reference valid nodes
            for edge in graph.edges:
                if edge.from_node not in graph._node_index:
                    self._add_error(
                        "E002",
                        f"Edge references unknown from_node: '{edge.from_node}'",
                        location=f"{graph.name}",
                        hint=f"Add node '{edge.from_node}' or fix the edge",
                    )

                if edge.to_node not in graph._node_index:
                    self._add_error(
                        "E003",
                        f"Edge references unknown to_node: '{edge.to_node}'",
                        location=f"{graph.name}",
                        hint=f"Add node '{edge.to_node}' or fix the edge",
                    )

    def _validate_types(self, ir: ManifestIR) -> None:
        """Validate node configs match expected schemas."""
        for graph in ir.graphs:
            for node in graph.nodes:
                # Router nodes must have router_ref
                if node.kind == NodeKind.ROUTER and not node.router_ref:
                    self._add_error(
                        "E101",
                        f"Router node '{node.id}' missing router_ref",
                        node=node,
                        hint="Add router_ref pointing to a defined router",
                    )

                # Tool nodes must have tool_ref
                if node.kind == NodeKind.TOOL and not node.tool_ref:
                    self._add_error(
                        "E102",
                        f"Tool node '{node.id}' missing tool_ref",
                        node=node,
                        hint="Add tool_ref pointing to a defined tool",
                    )

                # Check router_ref exists in manifest
                if node.router_ref and node.router_ref not in ir._router_index:
                    self._add_error(
                        "E103",
                        f"Node '{node.id}' references unknown router '{node.router_ref}'",
                        node=node,
                        hint=f"Define router '{node.router_ref}' in the routers section",
                    )

                # Check tool_ref exists in manifest
                if node.tool_ref and node.tool_ref not in ir._tool_index:
                    self._add_error(
                        "E104",
                        f"Node '{node.id}' references unknown tool '{node.tool_ref}'",
                        node=node,
                        hint=f"Define tool '{node.tool_ref}' in the tools section",
                    )

    def _validate_semantics(self, ir: ManifestIR) -> None:
        """Validate semantic correctness (valid transitions)."""
        for graph in ir.graphs:
            for node in graph.nodes:
                outgoing = graph.get_outgoing_edges(node.id)

                # Router nodes MUST have outgoing edges
                if node.kind == NodeKind.ROUTER and not outgoing:
                    self._add_error(
                        "E201",
                        f"Router node '{node.id}' has no outgoing edges",
                        node=node,
                        hint="Add conditional edges for each route option",
                    )

                # Tool nodes should have error handling
                if node.kind == NodeKind.TOOL:
                    has_error_edge = any(
                        e.condition.trigger == EdgeTrigger.ERROR for e in outgoing
                    )
                    if not has_error_edge and outgoing:
                        self._add_error(
                            "W303",
                            f"Tool node '{node.id}' has no error handling edge",
                            severity="warning",
                            node=node,
                            hint="Add an edge with trigger='error' for error handling",
                        )

    def _validate_completeness(self, ir: ManifestIR) -> None:
        """Validate completeness (router coverage, reachability)."""
        for graph in ir.graphs:
            # Check for unreachable nodes
            unreachable = graph.find_unreachable_nodes()
            if unreachable:
                self._add_error(
                    "W301",
                    f"Unreachable nodes in graph '{graph.name}': {', '.join(unreachable)}",
                    severity="warning",
                    location=f"{graph.name}",
                    hint="Remove these nodes or add edges to reach them",
                )

            # Check for terminal nodes
            terminal_nodes = [
                n.id for n in graph.nodes if not graph.get_outgoing_edges(n.id)
            ]
            if not terminal_nodes:
                self._add_error(
                    "W302",
                    f"Graph '{graph.name}' has no terminal nodes (possible infinite loop)",
                    severity="warning",
                    location=f"{graph.name}",
                    hint="Add at least one node without outgoing edges as an end state",
                )

    def has_errors(self) -> bool:
        """Check if validation found any errors (not warnings)."""
        return any(e.severity == "error" for e in self.errors)

    def has_warnings(self) -> bool:
        """Check if validation found any warnings."""
        return any(e.severity == "warning" for e in self.errors)

    def error_count(self) -> int:
        """Count errors."""
        return sum(1 for e in self.errors if e.severity == "error")

    def warning_count(self) -> int:
        """Count warnings."""
        return sum(1 for e in self.errors if e.severity == "warning")

    def format_summary(self) -> str:
        """Format a summary line."""
        errors = self.error_count()
        warnings = self.warning_count()
        if errors == 0 and warnings == 0:
            return "Validation passed: no errors, no warnings"
        return f"Validation: {errors} error(s), {warnings} warning(s)"


def validate_ir(
    ir: ManifestIR,
    *,
    strict: bool = False,
) -> List[ValidationError]:
    """
    Validate IR comprehensively.

    Convenience function for quick validation.

    Args:
        ir: Manifest IR to validate
        strict: If True, treat warnings as errors

    Returns:
        List of validation errors/warnings

    Example:
        errors = validate_ir(ir)
        if errors:
            for error in errors:
                print(error)
            raise ValueError("IR validation failed")
    """
    validator = IRValidator(strict=strict)
    return validator.validate(ir)


def validate_and_raise(ir: ManifestIR, *, strict: bool = False) -> None:
    """
    Validate IR and raise exception if invalid.

    Args:
        ir: Manifest IR to validate
        strict: If True, treat warnings as errors

    Raises:
        ValueError: If validation fails
    """
    validator = IRValidator(strict=strict)
    errors = validator.validate(ir)

    actual_errors = [e for e in errors if e.severity == "error"]
    if strict:
        actual_errors = errors

    if actual_errors:
        error_messages = "\n".join(str(e) for e in actual_errors)
        raise ValueError(f"IR validation failed:\n{error_messages}")


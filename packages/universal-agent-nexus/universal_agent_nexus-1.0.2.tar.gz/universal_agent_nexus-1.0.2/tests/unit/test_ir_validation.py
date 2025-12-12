"""
Tests for IR validation.
"""

import pytest

from universal_agent_nexus.ir import (
    EdgeCondition,
    EdgeIR,
    EdgeTrigger,
    GraphIR,
    ManifestIR,
    NodeIR,
    NodeKind,
    RouterIR,
    ToolIR,
)
from universal_agent_nexus.ir.validation import (
    IRValidator,
    ValidationError,
    validate_ir,
    validate_and_raise,
)


class TestIRValidator:
    """Test comprehensive IR validation."""

    def test_valid_ir_passes(self):
        """Test that valid IR passes validation."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test manifest",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                        NodeIR(id="end", kind=NodeKind.TASK, label="End"),
                    ],
                    edges=[
                        EdgeIR(
                            from_node="start",
                            to_node="end",
                            condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                        ),
                    ],
                )
            ],
        )

        errors = validate_ir(ir)
        actual_errors = [e for e in errors if e.severity == "error"]
        assert len(actual_errors) == 0

    def test_missing_entry_node(self):
        """Test detection of missing entry node."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="nonexistent",  # Does not exist
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                    ],
                    edges=[],
                )
            ],
        )

        errors = validate_ir(ir)
        assert any(e.code == "E001" for e in errors)

    def test_router_missing_router_ref(self):
        """Test detection of router node without router_ref."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="router",
                    nodes=[
                        NodeIR(
                            id="router",
                            kind=NodeKind.ROUTER,  # Router kind
                            label="Router",
                            router_ref=None,  # Missing!
                        ),
                    ],
                    edges=[],
                )
            ],
        )

        errors = validate_ir(ir)
        assert any(e.code == "E101" for e in errors)

    def test_tool_missing_tool_ref(self):
        """Test detection of tool node without tool_ref."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="tool",
                    nodes=[
                        NodeIR(
                            id="tool",
                            kind=NodeKind.TOOL,
                            label="Tool",
                            tool_ref=None,  # Missing!
                        ),
                    ],
                    edges=[],
                )
            ],
        )

        errors = validate_ir(ir)
        assert any(e.code == "E102" for e in errors)

    def test_unknown_router_ref(self):
        """Test detection of reference to undefined router."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="router",
                    nodes=[
                        NodeIR(
                            id="router",
                            kind=NodeKind.ROUTER,
                            label="Router",
                            router_ref="undefined_router",  # Does not exist
                        ),
                    ],
                    edges=[],
                )
            ],
            routers=[],  # No routers defined
        )

        errors = validate_ir(ir)
        assert any(e.code == "E103" for e in errors)

    def test_unknown_tool_ref(self):
        """Test detection of reference to undefined tool."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="tool",
                    nodes=[
                        NodeIR(
                            id="tool",
                            kind=NodeKind.TOOL,
                            label="Tool",
                            tool_ref="undefined_tool",  # Does not exist
                        ),
                    ],
                    edges=[],
                )
            ],
            tools=[],  # No tools defined
        )

        errors = validate_ir(ir)
        assert any(e.code == "E104" for e in errors)

    def test_router_no_outgoing_edges(self):
        """Test detection of router with no outgoing edges."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="router",
                    nodes=[
                        NodeIR(
                            id="router",
                            kind=NodeKind.ROUTER,
                            label="Router",
                            router_ref="my_router",
                        ),
                    ],
                    edges=[],  # No outgoing edges!
                )
            ],
            routers=[RouterIR(name="my_router")],
        )

        errors = validate_ir(ir)
        assert any(e.code == "E201" for e in errors)

    def test_unreachable_nodes_warning(self):
        """Test warning for unreachable nodes."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                        NodeIR(id="orphan", kind=NodeKind.TASK, label="Orphan"),
                    ],
                    edges=[],
                )
            ],
        )

        errors = validate_ir(ir)
        warnings = [e for e in errors if e.severity == "warning"]
        assert any(e.code == "W301" for e in warnings)

    def test_no_terminal_nodes_warning(self):
        """Test warning for graph with no terminal nodes."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="a",
                    nodes=[
                        NodeIR(id="a", kind=NodeKind.TASK, label="A"),
                        NodeIR(id="b", kind=NodeKind.TASK, label="B"),
                    ],
                    edges=[
                        EdgeIR(from_node="a", to_node="b"),
                        EdgeIR(from_node="b", to_node="a"),  # Cycle - no terminal!
                    ],
                )
            ],
        )

        errors = validate_ir(ir)
        warnings = [e for e in errors if e.severity == "warning"]
        assert any(e.code == "W302" for e in warnings)

    def test_validate_and_raise(self):
        """Test validate_and_raise helper."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="nonexistent",  # Error
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                    ],
                    edges=[],
                )
            ],
        )

        with pytest.raises(ValueError, match="IR validation failed"):
            validate_and_raise(ir)

    def test_validator_counts(self):
        """Test error and warning counts."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="nonexistent",  # Error
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                        NodeIR(id="orphan", kind=NodeKind.TASK, label="Orphan"),  # Warning
                    ],
                    edges=[],
                )
            ],
        )

        validator = IRValidator()
        validator.validate(ir)

        assert validator.error_count() >= 1
        assert validator.warning_count() >= 1
        assert validator.has_errors()
        assert validator.has_warnings()


class TestErrorFormatting:
    """Test error message formatting."""

    def test_error_string_format(self):
        """Test basic error string format."""
        error = ValidationError(
            severity="error",
            code="E001",
            message="Test error message",
        )

        assert "error" in str(error)
        assert "E001" in str(error)
        assert "Test error message" in str(error)

    def test_error_with_hint(self):
        """Test error with hint."""
        error = ValidationError(
            severity="error",
            code="E001",
            message="Test error",
            hint="Try doing X instead",
        )

        assert "hint" in str(error)
        assert "Try doing X instead" in str(error)

    def test_format_summary(self):
        """Test summary formatting."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                    ],
                    edges=[],
                )
            ],
        )

        validator = IRValidator()
        validator.validate(ir)

        summary = validator.format_summary()
        assert "error" in summary or "warning" in summary or "passed" in summary


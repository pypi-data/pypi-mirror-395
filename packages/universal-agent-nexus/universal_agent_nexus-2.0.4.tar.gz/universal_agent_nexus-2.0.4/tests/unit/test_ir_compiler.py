"""
Tests for IR-based compiler.

Tests the core IR types, parsers, generators, and transformations.
"""

import json
import pytest

from universal_agent_nexus.ir import (
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
from universal_agent_nexus.ir.parser import LangGraphParser, AWSParser, YAMLParser
from universal_agent_nexus.ir.generator import LangGraphGenerator, AWSGenerator, YAMLGenerator
from universal_agent_nexus.ir.transforms import (
    DeadNodeElimination,
    EdgeDeduplication,
    optimize,
)
from universal_agent_nexus.compiler import compile, parse, generate


class TestIRCoreTypes:
    """Test core IR types."""

    def test_node_ir_creation(self):
        """Test NodeIR creation."""
        node = NodeIR(
            id="test_node",
            kind=NodeKind.TASK,
            label="Test Node",
            description="A test node",
        )

        assert node.id == "test_node"
        assert node.kind == NodeKind.TASK
        assert node.label == "Test Node"

    def test_edge_ir_creation(self):
        """Test EdgeIR creation."""
        edge = EdgeIR(
            from_node="a",
            to_node="b",
            condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
        )

        assert edge.from_node == "a"
        assert edge.to_node == "b"
        assert edge.condition.trigger == EdgeTrigger.SUCCESS

    def test_graph_ir_validation(self):
        """Test GraphIR validation."""
        nodes = [
            NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
            NodeIR(id="end", kind=NodeKind.TASK, label="End"),
        ]
        edges = [
            EdgeIR(from_node="start", to_node="end"),
        ]

        graph = GraphIR(
            name="test",
            entry_node="start",
            nodes=nodes,
            edges=edges,
        )

        errors = graph.validate()
        assert len(errors) == 0

    def test_graph_ir_invalid_entry(self):
        """Test GraphIR with invalid entry node."""
        nodes = [NodeIR(id="a", kind=NodeKind.TASK, label="A")]

        graph = GraphIR(
            name="test",
            entry_node="nonexistent",
            nodes=nodes,
            edges=[],
        )

        errors = graph.validate()
        assert len(errors) > 0
        assert "nonexistent" in errors[0]

    def test_graph_find_unreachable_nodes(self):
        """Test finding unreachable nodes."""
        nodes = [
            NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
            NodeIR(id="middle", kind=NodeKind.TASK, label="Middle"),
            NodeIR(id="orphan", kind=NodeKind.TASK, label="Orphan"),  # Unreachable
        ]
        edges = [
            EdgeIR(from_node="start", to_node="middle"),
        ]

        graph = GraphIR(
            name="test",
            entry_node="start",
            nodes=nodes,
            edges=edges,
        )

        unreachable = graph.find_unreachable_nodes()
        assert "orphan" in unreachable
        assert "start" not in unreachable
        assert "middle" not in unreachable


class TestLangGraphParser:
    """Test LangGraph parser."""

    def test_parse_simple_graph(self):
        """Test parsing simple LangGraph code."""
        code = '''
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("start", start_fn)
graph.add_node("end", end_fn)
graph.add_edge("start", "end")
graph.set_entry_point("start")
'''
        parser = LangGraphParser()
        ir = parser.parse(code)

        assert ir.name
        assert len(ir.graphs) == 1
        assert len(ir.graphs[0].nodes) == 2
        assert ir.graphs[0].entry_node == "start"

    def test_parse_conditional_edges(self):
        """Test parsing conditional edges."""
        code = '''
graph = StateGraph(State)
graph.add_node("router", router_fn)
graph.add_node("a", a_fn)
graph.add_node("b", b_fn)
graph.add_conditional_edges("router", route_fn, {"option_a": "a", "option_b": "b"})
'''
        parser = LangGraphParser()
        ir = parser.parse(code)

        # Should have a router
        assert len(ir.routers) == 1
        assert ir.routers[0].name == "router_router"

        # Router node should be marked
        router_node = ir.graphs[0].get_node("router")
        assert router_node.kind == NodeKind.ROUTER

    def test_can_parse(self):
        """Test can_parse detection."""
        parser = LangGraphParser()

        assert parser.can_parse("from langgraph.graph import StateGraph")
        assert parser.can_parse("graph.add_node('x', fn)")
        assert not parser.can_parse('{"States": {}}')


class TestAWSParser:
    """Test AWS ASL parser."""

    def test_parse_simple_asl(self):
        """Test parsing simple ASL."""
        asl = {
            "Comment": "Test State Machine",
            "StartAt": "Process",
            "States": {
                "Process": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:::function:process",
                    "Next": "Complete",
                },
                "Complete": {
                    "Type": "Succeed",
                },
            },
        }

        parser = AWSParser()
        ir = parser.parse(json.dumps(asl))

        assert ir.name
        assert len(ir.graphs) == 1
        assert ir.graphs[0].entry_node == "Process"
        assert len(ir.graphs[0].nodes) == 2

    def test_parse_choice_state(self):
        """Test parsing Choice state."""
        asl = {
            "StartAt": "Router",
            "States": {
                "Router": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.type",
                            "StringEquals": "a",
                            "Next": "HandleA",
                        }
                    ],
                    "Default": "HandleDefault",
                },
                "HandleA": {"Type": "Succeed"},
                "HandleDefault": {"Type": "Succeed"},
            },
        }

        parser = AWSParser()
        ir = parser.parse(json.dumps(asl))

        router_node = ir.graphs[0].get_node("Router")
        assert router_node.kind == NodeKind.ROUTER

    def test_can_parse(self):
        """Test can_parse detection."""
        parser = AWSParser()

        assert parser.can_parse('{"States": {}, "StartAt": "X"}')
        assert not parser.can_parse("graph.add_node")


class TestGenerators:
    """Test code generators."""

    def test_langgraph_generator(self):
        """Test LangGraph code generation."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test agent",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                        NodeIR(id="end", kind=NodeKind.TASK, label="End"),
                    ],
                    edges=[
                        EdgeIR(from_node="start", to_node="end"),
                    ],
                )
            ],
        )

        generator = LangGraphGenerator()
        code = generator.generate(ir)

        assert "StateGraph" in code
        assert "add_node" in code
        assert "start" in code
        assert "end" in code

    def test_aws_generator(self):
        """Test AWS ASL generation."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test agent",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="process",
                    nodes=[
                        NodeIR(id="process", kind=NodeKind.TASK, label="Process"),
                    ],
                    edges=[],
                )
            ],
        )

        generator = AWSGenerator()
        asl_str = generator.generate(ir)
        asl = json.loads(asl_str)

        assert asl["StartAt"] == "process"
        assert "States" in asl
        assert "process" in asl["States"]

    def test_yaml_generator(self):
        """Test YAML generation."""
        ir = ManifestIR(
            name="test",
            version="1.0.0",
            description="Test agent",
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

        generator = YAMLGenerator()
        yaml_str = generator.generate(ir)

        assert "name: test" in yaml_str
        assert "entry_node: start" in yaml_str


class TestTransforms:
    """Test IR transformations."""

    def test_dead_node_elimination(self):
        """Test dead node elimination."""
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

        transform = DeadNodeElimination()
        result = transform.apply(ir)

        # Orphan should be removed
        assert len(result.graphs[0].nodes) == 1
        assert result.graphs[0].nodes[0].id == "start"

    def test_edge_deduplication(self):
        """Test edge deduplication."""
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
                        EdgeIR(from_node="a", to_node="b"),  # Duplicate
                        EdgeIR(from_node="a", to_node="b"),  # Duplicate
                    ],
                )
            ],
        )

        transform = EdgeDeduplication()
        result = transform.apply(ir)

        # Should have only 1 edge
        assert len(result.graphs[0].edges) == 1


class TestPassManager:
    """Test PassManager functionality."""

    def test_pass_manager_creation(self):
        """Test PassManager creation with optimization levels."""
        from universal_agent_nexus.ir.pass_manager import (
            PassManager,
            OptimizationLevel,
            create_default_pass_manager,
        )

        # Test all optimization levels
        for level in OptimizationLevel:
            manager = create_default_pass_manager(level)
            assert manager.opt_level == level

    def test_pass_manager_statistics(self):
        """Test pass statistics collection."""
        from universal_agent_nexus.ir.pass_manager import (
            PassManager,
            OptimizationLevel,
            create_default_pass_manager,
        )
        from universal_agent_nexus.ir.transforms import DeadNodeElimination

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

        manager = PassManager(opt_level=OptimizationLevel.BASIC, time_passes=True)
        manager.add(DeadNodeElimination())

        result = manager.run(ir)

        stats = manager.get_statistics()
        assert "dead-node-elimination" in stats
        assert stats["dead-node-elimination"].nodes_before == 2
        assert stats["dead-node-elimination"].nodes_after == 1

    def test_pass_manager_disable_pass(self):
        """Test disabling specific passes."""
        from universal_agent_nexus.ir.pass_manager import PassManager, OptimizationLevel
        from universal_agent_nexus.ir.transforms import DeadNodeElimination, EdgeDeduplication

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

        manager = PassManager(time_passes=True)
        manager.add(DeadNodeElimination())
        manager.disable("dead-node-elimination")  # Disable it

        result = manager.run(ir)

        # Pass should not have run
        assert "dead-node-elimination" not in manager.get_statistics()
        # Orphan node should still exist
        assert len(result.graphs[0].nodes) == 2


class TestAdvancedTransforms:
    """Test advanced optimization passes."""

    def test_constant_folding(self):
        """Test constant folding pass."""
        from universal_agent_nexus.ir.transforms import ConstantFolding

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
                        NodeIR(id="a", kind=NodeKind.TASK, label="A"),
                        NodeIR(id="b", kind=NodeKind.TASK, label="B"),
                    ],
                    edges=[
                        EdgeIR(
                            from_node="start",
                            to_node="a",
                            condition=EdgeCondition(
                                trigger=EdgeTrigger.SUCCESS, expression="True"
                            ),
                        ),
                        EdgeIR(
                            from_node="start",
                            to_node="b",
                            condition=EdgeCondition(
                                trigger=EdgeTrigger.SUCCESS, expression="False"
                            ),
                        ),
                    ],
                )
            ],
        )

        transform = ConstantFolding()
        result = transform.apply(ir)

        # Edge to "b" should be removed (False condition)
        assert len(result.graphs[0].edges) == 1
        assert result.graphs[0].edges[0].to_node == "a"


class TestCompiler:
    """Test unified compiler API."""

    def test_compile_langgraph_to_yaml(self):
        """Test compiling LangGraph to YAML."""
        code = '''
graph = StateGraph(State)
graph.add_node("start", start_fn)
graph.add_node("end", end_fn)
graph.add_edge("start", "end")
'''
        result = compile(code, source_type="langgraph", target="yaml")

        assert "name:" in result
        assert "start" in result
        assert "end" in result

    def test_compile_langgraph_to_aws(self):
        """Test compiling LangGraph to AWS ASL."""
        code = '''
graph = StateGraph(State)
graph.add_node("process", process_fn)
'''
        result = compile(code, source_type="langgraph", target="aws")
        asl = json.loads(result)

        assert "StartAt" in asl
        assert "States" in asl

    def test_compile_aws_to_langgraph(self):
        """Test BIDIRECTIONAL: AWS to LangGraph."""
        asl = json.dumps({
            "StartAt": "Process",
            "States": {
                "Process": {"Type": "Task", "Resource": "arn", "End": True},
            },
        })

        result = compile(asl, source_type="aws", target="langgraph")

        assert "StateGraph" in result
        assert "Process" in result

    def test_round_trip(self, tmp_path):
        """Test round-trip translation preserves structure."""
        original_code = '''
graph = StateGraph(State)
graph.add_node("analyze", analyze_fn)
graph.add_node("process", process_fn)
graph.add_edge("analyze", "process")
'''
        # LangGraph → YAML
        yaml_result = compile(original_code, source_type="langgraph", target="yaml")
        
        # Write YAML to temp file for second parse
        yaml_file = tmp_path / "temp_manifest.yaml"
        yaml_file.write_text(yaml_result)
        
        # YAML (file) → LangGraph  
        final_result = compile(str(yaml_file), source_type="yaml", target="langgraph")

        # Should preserve node names
        assert "analyze" in final_result
        assert "process" in final_result


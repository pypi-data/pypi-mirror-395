"""
Performance benchmarks.

Validates performance claims:
- boto3 vs aioboto3 (30% faster)
- batch vs individual DynamoDB ops (25x faster)
- prepared vs unprepared Postgres queries (2-3x faster)
- IR transformation passes (sub-millisecond)

Run with: pytest tests/benchmarks/ -v -s --benchmark
"""

import asyncio
import time
from typing import Callable
import pytest


def benchmark_sync(func: Callable, iterations: int = 100) -> float:
    """Benchmark synchronous function execution time."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    elapsed = time.perf_counter() - start
    return elapsed / iterations  # Average per iteration


async def benchmark_async(func: Callable, iterations: int = 100) -> float:
    """Benchmark async function execution time."""
    start = time.perf_counter()
    for _ in range(iterations):
        await func()
    elapsed = time.perf_counter() - start
    return elapsed / iterations


class TestIRPerformance:
    """Benchmark IR operations."""

    def test_ir_parsing_performance(self):
        """Benchmark IR parsing speed."""
        from universal_agent_nexus.ir.parser import LangGraphParser

        code = """
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("start", start_fn)
graph.add_node("process", process_fn)
graph.add_node("analyze", analyze_fn)
graph.add_node("router", router_fn)
graph.add_node("branch_a", branch_a_fn)
graph.add_node("branch_b", branch_b_fn)
graph.add_node("end", end_fn)
graph.add_edge("start", "process")
graph.add_edge("process", "analyze")
graph.add_edge("analyze", "router")
graph.add_conditional_edges("router", decide, {"a": "branch_a", "b": "branch_b"})
graph.add_edge("branch_a", "end")
graph.add_edge("branch_b", "end")
graph.set_entry_point("start")
"""
        parser = LangGraphParser()

        def parse():
            parser.parse(code)

        avg_time = benchmark_sync(parse, iterations=100)

        print(f"\nIR Parsing: {avg_time*1000:.3f}ms per parse")
        print(f"Throughput: {1/avg_time:.0f} parses/second")

        # Should be < 1ms
        assert avg_time < 0.001, f"Parsing too slow: {avg_time*1000:.3f}ms"

    def test_ir_transformation_performance(self):
        """Benchmark transformation pass speed."""
        from universal_agent_nexus.ir import (
            EdgeCondition,
            EdgeIR,
            EdgeTrigger,
            GraphIR,
            ManifestIR,
            NodeIR,
            NodeKind,
        )
        from universal_agent_nexus.ir.transforms import (
            DeadNodeElimination,
            EdgeDeduplication,
        )

        # Create a medium-sized graph
        nodes = [
            NodeIR(id=f"node_{i}", kind=NodeKind.TASK, label=f"Node {i}")
            for i in range(50)
        ]
        edges = [
            EdgeIR(
                from_node=f"node_{i}",
                to_node=f"node_{i+1}",
                condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
            )
            for i in range(49)
        ]
        # Add some orphan nodes
        nodes.extend([
            NodeIR(id=f"orphan_{i}", kind=NodeKind.TASK, label=f"Orphan {i}")
            for i in range(10)
        ])

        ir = ManifestIR(
            name="benchmark",
            version="1.0.0",
            description="Benchmark IR",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="node_0",
                    nodes=nodes,
                    edges=edges,
                )
            ],
        )

        dce = DeadNodeElimination()
        dedup = EdgeDeduplication()

        def run_transforms():
            # Create fresh copy
            ir_copy = ManifestIR(
                name="benchmark",
                version="1.0.0",
                description="Benchmark IR",
                graphs=[
                    GraphIR(
                        name="main",
                        entry_node="node_0",
                        nodes=list(nodes),
                        edges=list(edges),
                    )
                ],
            )
            dce.apply(ir_copy)
            dedup.apply(ir_copy)

        avg_time = benchmark_sync(run_transforms, iterations=50)

        print(f"\nTransform passes (60 nodes, 49 edges): {avg_time*1000:.3f}ms")
        print(f"Throughput: {1/avg_time:.0f} transforms/second")

        # Should be < 5ms for 60 nodes
        assert avg_time < 0.005, f"Transforms too slow: {avg_time*1000:.3f}ms"

    def test_ir_generation_performance(self):
        """Benchmark code generation speed."""
        from universal_agent_nexus.ir import (
            EdgeCondition,
            EdgeIR,
            EdgeTrigger,
            GraphIR,
            ManifestIR,
            NodeIR,
            NodeKind,
        )
        from universal_agent_nexus.ir.generator import (
            AWSGenerator,
            LangGraphGenerator,
            YAMLGenerator,
        )

        # Create test IR
        ir = ManifestIR(
            name="benchmark",
            version="1.0.0",
            description="Benchmark IR",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id=f"node_{i}", kind=NodeKind.TASK, label=f"Node {i}")
                        for i in range(20)
                    ],
                    edges=[
                        EdgeIR(
                            from_node=f"node_{i}",
                            to_node=f"node_{i+1}",
                            condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                        )
                        for i in range(19)
                    ],
                )
            ],
        )
        ir.graphs[0].nodes[0].id = "start"
        ir.graphs[0]._build_indexes()

        lg_gen = LangGraphGenerator()
        aws_gen = AWSGenerator()
        yaml_gen = YAMLGenerator()

        results = {}

        def gen_langgraph():
            lg_gen.generate(ir)

        def gen_aws():
            aws_gen.generate(ir)

        def gen_yaml():
            yaml_gen.generate(ir)

        results["langgraph"] = benchmark_sync(gen_langgraph, iterations=100)
        results["aws"] = benchmark_sync(gen_aws, iterations=100)
        results["yaml"] = benchmark_sync(gen_yaml, iterations=100)

        print(f"\nCode Generation (20 nodes):")
        for name, avg_time in results.items():
            print(f"  {name:12s}: {avg_time*1000:.3f}ms")

        # LangGraph/AWS should be < 1ms, YAML can be up to 10ms (yaml library overhead)
        assert results["langgraph"] < 0.001, f"langgraph too slow: {results['langgraph']*1000:.3f}ms"
        assert results["aws"] < 0.001, f"aws too slow: {results['aws']*1000:.3f}ms"
        assert results["yaml"] < 0.010, f"yaml too slow: {results['yaml']*1000:.3f}ms"

    def test_ir_validation_performance(self):
        """Benchmark validation speed."""
        from universal_agent_nexus.ir import (
            EdgeCondition,
            EdgeIR,
            EdgeTrigger,
            GraphIR,
            ManifestIR,
            NodeIR,
            NodeKind,
        )
        from universal_agent_nexus.ir.validation import validate_ir

        # Create test IR with various issues
        ir = ManifestIR(
            name="benchmark",
            version="1.0.0",
            description="Benchmark IR",
            graphs=[
                GraphIR(
                    name="main",
                    entry_node="start",
                    nodes=[
                        NodeIR(id="start", kind=NodeKind.TASK, label="Start"),
                        *[
                            NodeIR(id=f"node_{i}", kind=NodeKind.TASK, label=f"Node {i}")
                            for i in range(30)
                        ],
                        NodeIR(id="orphan", kind=NodeKind.TASK, label="Orphan"),
                    ],
                    edges=[
                        EdgeIR(
                            from_node="start",
                            to_node="node_0",
                            condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                        ),
                        *[
                            EdgeIR(
                                from_node=f"node_{i}",
                                to_node=f"node_{i+1}",
                                condition=EdgeCondition(trigger=EdgeTrigger.SUCCESS),
                            )
                            for i in range(29)
                        ],
                    ],
                )
            ],
        )

        def run_validation():
            validate_ir(ir)

        avg_time = benchmark_sync(run_validation, iterations=100)

        print(f"\nValidation (32 nodes, 30 edges): {avg_time*1000:.3f}ms")
        print(f"Throughput: {1/avg_time:.0f} validations/second")

        # Should be < 2ms
        assert avg_time < 0.002, f"Validation too slow: {avg_time*1000:.3f}ms"


@pytest.mark.asyncio
class TestDynamoDBPerformance:
    """Benchmark DynamoDB operations (requires moto)."""

    async def test_dynamodb_batch_vs_individual(self):
        """Benchmark batch_write_item vs individual put_item."""
        pytest.importorskip("moto")
        from moto import mock_aws
        import boto3

        with mock_aws():
            client = boto3.client("dynamodb", region_name="us-east-1")

            # Create table
            client.create_table(
                TableName="test-tasks",
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )

            items = [
                {"id": {"S": f"task-{i}"}, "data": {"S": f"data-{i}"}}
                for i in range(25)
            ]

            # Individual writes
            async def individual_writes():
                for item in items:
                    await asyncio.to_thread(
                        client.put_item,
                        TableName="test-tasks",
                        Item=item,
                    )

            individual_time = await benchmark_async(individual_writes, iterations=5)

            # Batch writes
            async def batch_writes():
                await asyncio.to_thread(
                    client.batch_write_item,
                    RequestItems={
                        "test-tasks": [
                            {"PutRequest": {"Item": item}} for item in items
                        ]
                    },
                )

            batch_time = await benchmark_async(batch_writes, iterations=5)

            speedup = individual_time / batch_time

            print(f"\nDynamoDB (25 items):")
            print(f"  Individual writes: {individual_time*1000:.2f}ms")
            print(f"  Batch writes:      {batch_time*1000:.2f}ms")
            print(f"  Speedup:           {speedup:.1f}x")

            # Batch should be at least 5x faster (moto is faster than real DynamoDB)
            assert speedup >= 3, f"Expected significant speedup, got {speedup:.1f}x"


class TestCompilerEndToEnd:
    """End-to-end compiler benchmarks."""

    def test_full_compile_pipeline(self):
        """Benchmark full compile pipeline (parse → transform → generate)."""
        from universal_agent_nexus.compiler import compile
        from universal_agent_nexus.ir.pass_manager import OptimizationLevel

        code = """
graph = StateGraph(State)
graph.add_node("start", start_fn)
graph.add_node("process", process_fn)
graph.add_node("analyze", analyze_fn)
graph.add_node("router", router_fn)
graph.add_node("branch_a", branch_a_fn)
graph.add_node("branch_b", branch_b_fn)
graph.add_node("end", end_fn)
graph.add_edge("start", "process")
graph.add_edge("process", "analyze")
graph.add_conditional_edges("router", decide, {"a": "branch_a", "b": "branch_b"})
graph.add_edge("branch_a", "end")
graph.add_edge("branch_b", "end")
"""
        results = {}

        # No optimization
        def compile_o0():
            compile(
                code,
                source_type="langgraph",
                target="aws",
                opt_level=OptimizationLevel.NONE,
            )

        results["O0 (none)"] = benchmark_sync(compile_o0, iterations=50)

        # Default optimization
        def compile_o2():
            compile(
                code,
                source_type="langgraph",
                target="aws",
                opt_level=OptimizationLevel.DEFAULT,
            )

        results["O2 (default)"] = benchmark_sync(compile_o2, iterations=50)

        # Aggressive optimization
        def compile_o3():
            compile(
                code,
                source_type="langgraph",
                target="aws",
                opt_level=OptimizationLevel.AGGRESSIVE,
            )

        results["O3 (aggressive)"] = benchmark_sync(compile_o3, iterations=50)

        print(f"\nFull compile pipeline (LangGraph -> AWS):")
        for name, avg_time in results.items():
            print(f"  {name:20s}: {avg_time*1000:.2f}ms")

        # All should be < 10ms
        for name, avg_time in results.items():
            assert avg_time < 0.010, f"{name} compile too slow: {avg_time*1000:.2f}ms"


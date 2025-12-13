"""
Universal Agent Compiler.

Unified translation API using IR.
This is the PUBLIC API - users interact with this, not parsers/generators directly.

Architecture:
    Parser → IR → Transform → Generator

Example:
    # Any-to-any translation
    from universal_agent_nexus.compiler import compile

    # LangGraph → AWS (bidirectional!)
    compile("agent.py", target="aws", output="state_machine.json")

    # AWS → LangGraph (reverse!)
    compile("state_machine.json", target="langgraph", output="agent.py")

    # Any → UAA YAML (for Fabric enrichment)
    compile("agent.py", target="uaa", output="manifest.yaml")
"""

import logging
from pathlib import Path
from typing import Literal, Optional, Union

from universal_agent_nexus.ir import ManifestIR
from universal_agent_nexus.ir.parser import PARSERS  # For backwards compatibility
from universal_agent_nexus.parser_registry import (
    detect_source_type,
    get_parser,
    list_parsers as list_parsers_from_registry,
)
from universal_agent_nexus.ir.generator import GENERATORS  # For backwards compatibility
from universal_agent_nexus.generator_registry import (
    get_generator,
    list_generators as list_generators_from_registry,
)
from universal_agent_nexus.ir.transforms import (
    TransformPipeline,
    create_full_pipeline,
    create_optimization_pipeline,
    optimize,
)
from universal_agent_nexus.ir.pass_manager import (
    PassManager,
    OptimizationLevel,
    create_default_pass_manager,
)

logger = logging.getLogger(__name__)

SourceType = Literal["langgraph", "aws", "yaml", "uaa", "auto"]
TargetType = Literal["langgraph", "aws", "yaml", "uaa"]


def compile(
    source: str,
    *,
    target: TargetType = "uaa",
    source_type: SourceType = "auto",
    output: Optional[str] = None,
    optimize_ir: bool = True,
    validate_ir: bool = True,
    opt_level: OptimizationLevel = OptimizationLevel.DEFAULT,
) -> str:
    """
    Universal compilation: any source → any target.

    This is the MAGIC - IR enables bidirectional translation!

    Examples:
        # LangGraph → AWS
        compile("agent.py", target="aws")

        # AWS → LangGraph (BIDIRECTIONAL!)
        compile("state_machine.json", target="langgraph")

        # Any → UAA YAML (for Fabric enrichment)
        compile("agent.py", target="uaa")

        # Write to file
        compile("agent.py", target="aws", output="state_machine.json")

        # With optimization level
        compile("agent.py", target="aws", opt_level=OptimizationLevel.AGGRESSIVE)

    Args:
        source: Path to source file or source string
        target: Target format (langgraph, aws, yaml/uaa)
        source_type: Source format (auto-detect if not specified)
        output: Optional output file path
        optimize_ir: Apply optimization passes
        validate_ir: Apply validation passes
        opt_level: Optimization level (NONE, BASIC, DEFAULT, AGGRESSIVE)

    Returns:
        Generated code/config as string
    """
    logger.info(f"Compiling {source} → {target} (opt_level={opt_level.name})")

    # Step 1: Parse source → IR
    ir = parse(source, source_type=source_type)

    # Step 2: Transform IR using PassManager
    if validate_ir or optimize_ir:
        # Use PassManager for proper dependency resolution
        if not optimize_ir:
            opt_level = OptimizationLevel.NONE

        manager = create_default_pass_manager(opt_level)
        ir = manager.run(ir)

        # Log statistics
        stats = manager.get_statistics()
        if stats:
            total_time = sum(s.elapsed_ms for s in stats.values())
            logger.info(f"Applied {len(stats)} passes in {total_time:.2f}ms")

    # Step 3: Generate target format
    result = generate(ir, target=target)

    # Step 4: Write to file if requested
    if output:
        Path(output).write_text(result, encoding="utf-8")
        logger.info(f"Wrote output to {output}")

    return result


def parse(
    source: str,
    *,
    source_type: SourceType = "auto",
) -> ManifestIR:
    """
    Parse source into IR.

    Lower-level API for when you need the IR directly.

    Args:
        source: Path to source file or source string
        source_type: Source format (auto-detect if not specified)

    Returns:
        ManifestIR
    """
    # Auto-detect source type
    if source_type == "auto":
        source_type = detect_source_type(source)
        logger.info(f"Detected source type: {source_type}")

    # Get parser
    parser = get_parser(source_type)
    logger.debug(f"Using parser: {type(parser).__name__}")

    # Parse
    ir = parser.parse(source)
    logger.info(
        f"Parsed: {len(ir.graphs)} graph(s), "
        f"{sum(len(g.nodes) for g in ir.graphs)} nodes, "
        f"{len(ir.tools)} tools"
    )

    return ir


def generate(
    ir: ManifestIR,
    *,
    target: TargetType = "uaa",
) -> str:
    """
    Generate target format from IR.

    Lower-level API for when you have IR directly.

    Args:
        ir: ManifestIR
        target: Target format

    Returns:
        Generated code/config as string
    """
    # Get generator
    generator = get_generator(target)
    logger.debug(f"Using generator: {type(generator).__name__}")

    # Generate
    result = generator.generate(ir)
    logger.info(f"Generated {len(result)} bytes of {target} code")

    return result


def translate(
    source: str,
    *,
    target: TargetType = "uaa",
    source_type: SourceType = "auto",
    output: Optional[str] = None,
    optimize_ir: bool = True,
) -> str:
    """
    Alias for compile() - for backwards compatibility.

    See compile() for full documentation.
    """
    return compile(
        source,
        target=target,
        source_type=source_type,
        output=output,
        optimize_ir=optimize_ir,
    )


# ===== CONVENIENCE FUNCTIONS =====


def langgraph_to_aws(source: str, output: Optional[str] = None) -> str:
    """Convert LangGraph Python → AWS Step Functions ASL."""
    return compile(source, target="aws", source_type="langgraph", output=output)


def aws_to_langgraph(source: str, output: Optional[str] = None) -> str:
    """Convert AWS Step Functions ASL → LangGraph Python."""
    return compile(source, target="langgraph", source_type="aws", output=output)


def to_uaa(source: str, output: Optional[str] = None) -> str:
    """Convert any format → UAA YAML (for Fabric enrichment)."""
    return compile(source, target="uaa", output=output)


def from_uaa(source: str, target: TargetType, output: Optional[str] = None) -> str:
    """Convert UAA YAML → any target format."""
    return compile(source, target=target, source_type="uaa", output=output)


# ===== INFO FUNCTIONS =====


def list_source_types() -> list[str]:
    """List available source types."""
    # Use registry if available, fallback to PARSERS for backwards compatibility
    try:
        parser_info = list_parsers_from_registry()
        return list(parser_info.keys())
    except Exception:
        return list(PARSERS.keys())


def list_target_types() -> list[str]:
    """List available target types."""
    # Use registry if available, fallback to GENERATORS for backwards compatibility
    try:
        generator_info = list_generators_from_registry()
        return list(generator_info.keys())
    except Exception:
        return list(GENERATORS.keys())


def get_compiler_info() -> dict:
    """Get compiler information."""
    return {
        "version": "1.0.0",
        "source_types": list_source_types(),
        "target_types": list_target_types(),
        "transforms": [
            "dead-node-elimination",
            "edge-deduplication",
            "condition-simplification",
            "router-validation",
            "tool-validation",
            "cycle-detection",
            "empty-graph-removal",
        ],
    }


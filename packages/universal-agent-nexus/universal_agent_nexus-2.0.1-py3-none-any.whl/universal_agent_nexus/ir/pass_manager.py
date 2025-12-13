"""
Pass manager for controlling transformation pipeline.

Inspired by LLVM PassManager architecture.

Features:
- Optimization levels (-O0, -O1, -O2, -O3)
- Pass dependency resolution
- Pass filtering (enable/disable specific passes)
- Pass statistics (time, memory, IR changes)
- Pass verification (sanity checks)

Example:
    manager = create_default_pass_manager(OptimizationLevel.AGGRESSIVE)
    ir = manager.run(ir)
    print(manager.get_statistics())
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

from . import ManifestIR

logger = logging.getLogger(__name__)


class OptimizationLevel(Enum):
    """
    Optimization levels (like -O0, -O1, -O2, -O3).

    NONE: No optimizations - fastest compilation
    BASIC: Fast, safe optimizations
    DEFAULT: Balanced optimization/compilation speed
    AGGRESSIVE: Maximum optimization - may increase compile time
    """

    NONE = 0
    BASIC = 1
    DEFAULT = 2
    AGGRESSIVE = 3


@dataclass
class PassMetadata:
    """Metadata for transformation pass."""

    name: str
    description: str
    requires: Set[str] = field(default_factory=set)  # Must run after these
    invalidates: Set[str] = field(default_factory=set)  # Invalidates these passes
    preserves: Set[str] = field(default_factory=set)  # Preserves these analyses


@dataclass
class PassStatistics:
    """Statistics for a single pass execution."""

    elapsed_ms: float
    nodes_before: int
    nodes_after: int
    edges_before: int
    edges_after: int

    @property
    def nodes_removed(self) -> int:
        return self.nodes_before - self.nodes_after

    @property
    def edges_removed(self) -> int:
        return self.edges_before - self.edges_after


class PassManager:
    """
    Manage transformation pipeline execution.

    Features:
    - Optimization levels (-O0, -O1, -O2, -O3)
    - Pass filtering (enable/disable specific passes)
    - Pass statistics (time, memory, IR changes)
    - Pass verification (sanity checks)

    Example:
        from universal_agent_nexus.ir.pass_manager import (
            PassManager,
            OptimizationLevel,
        )

        manager = PassManager(opt_level=OptimizationLevel.AGGRESSIVE)
        manager.add(DeadNodeElimination())
        manager.add(EdgeDeduplication())

        ir = manager.run(ir)
        print(manager.get_statistics())
    """

    def __init__(
        self,
        *,
        opt_level: OptimizationLevel = OptimizationLevel.DEFAULT,
        verify_ir: bool = True,
        time_passes: bool = True,
    ):
        self.opt_level = opt_level
        self.verify_ir = verify_ir
        self.time_passes = time_passes
        self.passes: List = []
        self.disabled_passes: Set[str] = set()
        self._statistics: Dict[str, PassStatistics] = {}

    def add(self, transform) -> "PassManager":
        """
        Add transformation pass.

        Args:
            transform: Transform instance

        Returns:
            Self for chaining
        """
        self.passes.append(transform)
        return self

    def add_custom_pass(
        self,
        pass_instance,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> "PassManager":
        """
        Add custom pass with optional ordering constraints.

        Args:
            pass_instance: Transform instance
            before: Run before this pass (by name)
            after: Run after this pass (by name)

        Returns:
            Self for chaining

        Example:
            manager = PassManager()
            manager.add_custom_pass(MyCustomPass(), after="dead-node-elimination")
        """
        # Store ordering constraints in metadata if needed
        # For now, just add to passes - dependency resolution will handle ordering
        if before or after:
            # Store constraints in a way that _resolve_dependencies can use
            # We'll enhance metadata to include explicit ordering
            pass_instance._ordering_before = before
            pass_instance._ordering_after = after

        self.passes.append(pass_instance)
        return self

    def get_pass(self, name: str) -> Optional:
        """
        Get pass by name.

        Args:
            name: Pass name

        Returns:
            Transform instance or None if not found
        """
        for transform in self.passes:
            if transform.name == name:
                return transform
        return None

    def list_passes(self) -> Dict[str, PassMetadata]:
        """
        List all passes with metadata.

        Returns:
            {pass_name: PassMetadata(...)}
        """
        result = {}
        for transform in self.passes:
            if hasattr(transform, 'metadata'):
                result[transform.name] = transform.metadata
            else:
                # Fallback for passes without metadata
                from .transforms import PassMetadata
                result[transform.name] = PassMetadata(
                    name=transform.name,
                    description=f"Pass: {transform.name}",
                )
        return result

    def disable(self, pass_name: str) -> "PassManager":
        """Disable specific pass."""
        self.disabled_passes.add(pass_name)
        return self

    def enable(self, pass_name: str) -> "PassManager":
        """Re-enable specific pass."""
        self.disabled_passes.discard(pass_name)
        return self

    def run(self, ir: ManifestIR) -> ManifestIR:
        """Execute pipeline with dependency resolution."""
        # Resolve dependencies and sort passes
        sorted_passes = self._resolve_dependencies()

        for transform in sorted_passes:
            pass_name = transform.name

            # Skip disabled passes
            if pass_name in self.disabled_passes:
                logger.debug(f"Skipping disabled pass: {pass_name}")
                continue

            # Count nodes/edges before
            nodes_before = sum(len(g.nodes) for g in ir.graphs)
            edges_before = sum(len(g.edges) for g in ir.graphs)

            # Time pass execution
            start = time.perf_counter()
            ir = transform.apply(ir)
            elapsed = (time.perf_counter() - start) * 1000  # ms

            # Count nodes/edges after
            nodes_after = sum(len(g.nodes) for g in ir.graphs)
            edges_after = sum(len(g.edges) for g in ir.graphs)

            # Verify IR
            if self.verify_ir:
                self._verify_ir(ir, pass_name)

            # Record statistics
            if self.time_passes:
                self._statistics[pass_name] = PassStatistics(
                    elapsed_ms=elapsed,
                    nodes_before=nodes_before,
                    nodes_after=nodes_after,
                    edges_before=edges_before,
                    edges_after=edges_after,
                )

                logger.debug(
                    f"Pass {pass_name}: {elapsed:.2f}ms, "
                    f"nodes {nodes_before}→{nodes_after}, "
                    f"edges {edges_before}→{edges_after}"
                )

        return ir

    def get_statistics(self) -> Dict[str, PassStatistics]:
        """Get pass statistics."""
        return self._statistics

    def print_statistics(self) -> None:
        """Print pass statistics to console."""
        if not self._statistics:
            print("No statistics collected (time_passes=False?)")
            return

        print("\n=== Pass Statistics ===")
        total_time = 0.0
        for name, stats in self._statistics.items():
            print(
                f"  {name:30s} {stats.elapsed_ms:8.2f}ms  "
                f"nodes: {stats.nodes_before:3d}→{stats.nodes_after:3d}  "
                f"edges: {stats.edges_before:3d}→{stats.edges_after:3d}"
            )
            total_time += stats.elapsed_ms
        print(f"  {'TOTAL':30s} {total_time:8.2f}ms")

    def _resolve_dependencies(self) -> List:
        """
        Topologically sort passes based on dependencies.

        Uses pass metadata to determine execution order.
        If a pass A requires pass B, then B runs before A.
        Also handles explicit before/after constraints.
        """
        # Build dependency graph: pass_name -> set of passes it requires
        pass_map = {p.name: p for p in self.passes}
        requirements: Dict[str, Set[str]] = {}

        for p in self.passes:
            deps = set()
            if hasattr(p, "metadata") and p.metadata:
                # Only consider requirements that are actually in our pass list
                deps = p.metadata.requires.intersection(pass_map.keys())
            
            # Handle explicit ordering constraints
            if hasattr(p, "_ordering_after") and p._ordering_after:
                after_name = p._ordering_after
                if after_name in pass_map:
                    deps.add(after_name)
            
            if hasattr(p, "_ordering_before") and p._ordering_before:
                before_name = p._ordering_before
                if before_name in pass_map:
                    # This pass must run before 'before_name', so 'before_name' requires this
                    if before_name not in requirements:
                        requirements[before_name] = set()
                    requirements[before_name].add(p.name)
            
            if p.name not in requirements:
                requirements[p.name] = set()
            requirements[p.name].update(deps)

        # Kahn's algorithm for topological sort
        # in_degree[X] = number of passes that X requires (not yet processed)
        in_degree = {name: len(deps) for name, deps in requirements.items()}

        # Start with passes that have no requirements (in_degree = 0)
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            name = queue.pop(0)
            result.append(name)

            # For each pass that requires this one, decrement their in_degree
            for other_name, other_deps in requirements.items():
                if name in other_deps:
                    in_degree[other_name] -= 1
                    if in_degree[other_name] == 0:
                        queue.append(other_name)

        if len(result) != len(requirements):
            # Circular dependency - fall back to original order
            logger.debug(
                "Dependency resolution incomplete (%d/%d), using original pass order",
                len(result),
                len(requirements),
            )
            return self.passes

        return [pass_map[name] for name in result]

    def _verify_ir(self, ir: ManifestIR, pass_name: str) -> None:
        """Verify IR is well-formed after pass."""
        errors = ir.validate()
        if errors:
            error_msg = "; ".join(errors)
            raise RuntimeError(f"Pass '{pass_name}' produced invalid IR: {error_msg}")


# ===== FACTORY FUNCTIONS =====


def create_default_pass_manager(
    opt_level: OptimizationLevel = OptimizationLevel.DEFAULT,
    *,
    enable_batching: bool = False,
) -> PassManager:
    """
    Create pass manager with default passes for optimization level.

    Args:
        opt_level: Optimization level
        enable_batching: Whether to enable batch optimization pass

    Returns:
        Configured PassManager
    """
    from .transforms import (
        CycleDetection,
        DeadNodeElimination,
        EdgeDeduplication,
        ConditionSimplification,
        RouterValidation,
        ToolValidation,
    )

    manager = PassManager(opt_level=opt_level, verify_ir=True)

    if opt_level == OptimizationLevel.NONE:
        # No optimization passes
        pass

    elif opt_level == OptimizationLevel.BASIC:
        # Fast, safe optimizations
        manager.add(DeadNodeElimination())
        manager.add(EdgeDeduplication())

    elif opt_level == OptimizationLevel.DEFAULT:
        # Balanced optimization
        manager.add(DeadNodeElimination())
        manager.add(EdgeDeduplication())
        manager.add(ConditionSimplification())
        manager.add(RouterValidation())
        manager.add(ToolValidation())

    elif opt_level == OptimizationLevel.AGGRESSIVE:
        # Maximum optimization
        manager.add(DeadNodeElimination())
        manager.add(EdgeDeduplication())
        manager.add(ConditionSimplification())
        manager.add(RouterValidation())
        manager.add(ToolValidation())
        manager.add(CycleDetection())

    # Add batch optimization if enabled
    if enable_batching:
        from .passes.batch_optimization import BatchOptimizationPass
        manager.add(BatchOptimizationPass())

    return manager


"""
Compiler Builder Pattern for advanced configuration.

Enables configuring compiler with custom components:
- Custom parsers and generators
- Custom optimization passes
- Custom tool/router factories
- Fine-grained control over compilation pipeline
"""

from typing import Optional, Set

from .generator_registry import GeneratorRegistry, get_registry as get_generator_registry
from .ir.factories import RouterFactory, ToolFactory, get_router_factory, get_tool_factory
from .ir.pass_manager import OptimizationLevel, PassManager
from .parser_registry import ParserRegistry, get_registry as get_parser_registry


class CompilerBuilder:
    """
    Builder for configuring compiler with custom components.

    Usage:
        builder = CompilerBuilder()
        builder.register_parser("my_format", MyParser())
        builder.register_generator("my_target", MyGenerator())
        builder.with_optimization_level(OptimizationLevel.AGGRESSIVE)
        builder.with_tool_factory(CustomToolFactory())

        result = builder.compile("agent.py", target="my_target")
        
    With batch optimization:
        builder = CompilerBuilder()
        builder.with_batch_optimization()
        result = builder.compile("agent.yaml", target="langgraph")
    """

    def __init__(self):
        self._parser_registry: Optional[ParserRegistry] = None
        self._generator_registry: Optional[GeneratorRegistry] = None
        self._pass_manager: Optional[PassManager] = None
        self._tool_factory: Optional[ToolFactory] = None
        self._router_factory: Optional[RouterFactory] = None
        self._optimization_level = OptimizationLevel.DEFAULT
        self._validate_ir = True
        self._optimize_ir = True
        self._enable_batching = False

    def register_parser(
        self,
        source_type: str,
        parser,
        *,
        detection_priority: int = 100,
        aliases: Optional[Set[str]] = None,
        description: Optional[str] = None,
    ) -> "CompilerBuilder":
        """
        Register custom parser.

        Args:
            source_type: Unique identifier (e.g., "langgraph", "airflow")
            parser: Parser implementation
            detection_priority: Higher = checked first in auto-detect
            aliases: Alternative names
            description: Human-readable description

        Returns:
            Self for chaining
        """
        if self._parser_registry is None:
            self._parser_registry = ParserRegistry()
            # Copy defaults from global registry
            default_registry = get_parser_registry()
            for source_type_existing, parser_existing in default_registry._parsers.items():
                info = default_registry._info.get(source_type_existing)
                if info:
                    self._parser_registry.register(
                        source_type_existing,
                        parser_existing,
                        detection_priority=info.detection_priority,
                        aliases=info.aliases,
                        description=info.description,
                    )

        self._parser_registry.register(
            source_type,
            parser,
            detection_priority=detection_priority,
            aliases=aliases,
            description=description,
        )
        return self

    def register_generator(
        self,
        target_type: str,
        generator,
        *,
        aliases: Optional[Set[str]] = None,
        default_options: Optional[dict] = None,
        description: Optional[str] = None,
    ) -> "CompilerBuilder":
        """
        Register custom generator.

        Args:
            target_type: Unique identifier (e.g., "langgraph", "temporal")
            generator: Generator implementation
            aliases: Alternative names
            default_options: Default generation options
            description: Human-readable description

        Returns:
            Self for chaining
        """
        if self._generator_registry is None:
            self._generator_registry = GeneratorRegistry()
            # Copy defaults from global registry
            default_registry = get_generator_registry()
            for target_type_existing, generator_existing in default_registry._generators.items():
                info = default_registry._info.get(target_type_existing)
                if info:
                    self._generator_registry.register(
                        target_type_existing,
                        generator_existing,
                        aliases=info.aliases,
                        default_options=info.default_options,
                        description=info.description,
                    )

        self._generator_registry.register(
            target_type,
            generator,
            aliases=aliases,
            default_options=default_options,
            description=description,
        )
        return self

    def with_optimization_level(self, level: OptimizationLevel) -> "CompilerBuilder":
        """
        Set optimization level.

        Args:
            level: Optimization level (NONE, BASIC, DEFAULT, AGGRESSIVE)

        Returns:
            Self for chaining
        """
        self._optimization_level = level
        return self

    def with_tool_factory(self, factory: ToolFactory) -> "CompilerBuilder":
        """
        Set tool factory.

        Args:
            factory: ToolFactory instance

        Returns:
            Self for chaining
        """
        self._tool_factory = factory
        return self

    def with_router_factory(self, factory: RouterFactory) -> "CompilerBuilder":
        """
        Set router factory.

        Args:
            factory: RouterFactory instance

        Returns:
            Self for chaining
        """
        self._router_factory = factory
        return self

    def add_optimization_pass(self, transform) -> "CompilerBuilder":
        """
        Add custom optimization pass.

        Args:
            transform: Transform instance

        Returns:
            Self for chaining
        """
        if self._pass_manager is None:
            from .ir.pass_manager import create_default_pass_manager

            self._pass_manager = create_default_pass_manager(self._optimization_level)

        self._pass_manager.add(transform)
        return self

    def with_validation(self, enabled: bool = True) -> "CompilerBuilder":
        """
        Enable/disable IR validation.

        Args:
            enabled: Whether to validate IR

        Returns:
            Self for chaining
        """
        self._validate_ir = enabled
        return self

    def with_optimization(self, enabled: bool = True) -> "CompilerBuilder":
        """
        Enable/disable optimization.

        Args:
            enabled: Whether to optimize IR

        Returns:
            Self for chaining
        """
        self._optimize_ir = enabled
        return self

    def with_batch_optimization(
        self,
        enabled: bool = True,
        batch_size: int = 100,
        max_wait_ms: float = 5000.0,
    ) -> "CompilerBuilder":
        """
        Enable batch optimization for Anthropic Batch API.

        When enabled, the compiler will:
        1. Analyze IR for LLM call nodes
        2. Annotate them with BatchAnnotation for runtime batching
        3. Enable cost optimization via Anthropic Batch API

        Args:
            enabled: Whether to enable batch optimization
            batch_size: Target batch size for grouping
            max_wait_ms: Max wait time for batch accumulation

        Returns:
            Self for chaining

        Example:
            builder = CompilerBuilder()
            builder.with_batch_optimization(batch_size=50)
            result = builder.compile("agent.yaml", target="langgraph")
        """
        self._enable_batching = enabled

        if enabled:
            # Add batch optimization pass
            from .ir.passes.batch_optimization import BatchOptimizationPass

            batch_pass = BatchOptimizationPass(
                batch_size=batch_size,
                max_wait_ms=max_wait_ms,
            )
            self.add_optimization_pass(batch_pass)

        return self

    def build(self) -> "Compiler":
        """
        Build configured compiler.

        Returns:
            Configured Compiler instance
        """
        return Compiler(
            parser_registry=self._parser_registry,
            generator_registry=self._generator_registry,
            pass_manager=self._pass_manager,
            tool_factory=self._tool_factory,
            router_factory=self._router_factory,
            optimization_level=self._optimization_level,
            validate_ir=self._validate_ir,
            optimize_ir=self._optimize_ir,
        )


class Compiler:
    """Configured compiler instance."""

    def __init__(
        self,
        parser_registry: Optional[ParserRegistry],
        generator_registry: Optional[GeneratorRegistry],
        pass_manager: Optional[PassManager],
        tool_factory: Optional[ToolFactory],
        router_factory: Optional[RouterFactory],
        optimization_level: OptimizationLevel,
        validate_ir: bool,
        optimize_ir: bool,
    ):
        self.parser_registry = parser_registry
        self.generator_registry = generator_registry
        self.pass_manager = pass_manager
        self.tool_factory = tool_factory
        self.router_factory = router_factory
        self.optimization_level = optimization_level
        self.validate_ir = validate_ir
        self.optimize_ir = optimize_ir

    def compile(
        self,
        source: str,
        *,
        target: str = "uaa",
        source_type: str = "auto",
        output: Optional[str] = None,
    ) -> str:
        """
        Compile with configured components.

        Args:
            source: Path to source file or source string
            target: Target format
            source_type: Source format (auto-detect if not specified)
            output: Optional output file path

        Returns:
            Generated code/config as string
        """
        import logging
        from pathlib import Path

        from .ir import ManifestIR

        logger = logging.getLogger(__name__)

        # Use custom registries if provided, otherwise use global
        if self.parser_registry:
            if source_type == "auto":
                detected = self.parser_registry.detect(source)
                if detected is None:
                    raise ValueError(f"Cannot detect source type for: {source}")
                source_type = detected
            parser = self.parser_registry.get(source_type)
            if parser is None:
                raise ValueError(f"Unknown source type: {source_type}")
        else:
            from .parser_registry import detect_source_type, get_parser

            if source_type == "auto":
                source_type = detect_source_type(source)
            parser = get_parser(source_type)

        # Temporarily set factories if custom ones provided
        old_tool_factory = None
        old_router_factory = None
        if self.tool_factory:
            from .ir.factories import get_tool_factory, set_tool_factory

            old_tool_factory = get_tool_factory()
            set_tool_factory(self.tool_factory)
        if self.router_factory:
            from .ir.factories import get_router_factory, set_router_factory

            old_router_factory = get_router_factory()
            set_router_factory(self.router_factory)

        try:
            # Parse
            ir = parser.parse(source)
            logger.info(
                f"Parsed: {len(ir.graphs)} graph(s), "
                f"{sum(len(g.nodes) for g in ir.graphs)} nodes, "
                f"{len(ir.tools)} tools"
            )

            # Transform
            if self.validate_ir or self.optimize_ir:
                if self.pass_manager:
                    manager = self.pass_manager
                else:
                    from .ir.pass_manager import create_default_pass_manager

                    opt_level = (
                        OptimizationLevel.NONE if not self.optimize_ir else self.optimization_level
                    )
                    manager = create_default_pass_manager(opt_level)

                ir = manager.run(ir)

                # Log statistics
                stats = manager.get_statistics()
                if stats:
                    total_time = sum(s.elapsed_ms for s in stats.values())
                    logger.info(f"Applied {len(stats)} passes in {total_time:.2f}ms")

            # Generate
            if self.generator_registry:
                generator = self.generator_registry.get(target)
                if generator is None:
                    raise ValueError(f"Unknown target type: {target}")
            else:
                from .generator_registry import get_generator

                generator = get_generator(target)

            result = generator.generate(ir)
            logger.info(f"Generated {len(result)} bytes of {target} code")

            # Write to file if requested
            if output:
                Path(output).write_text(result, encoding="utf-8")
                logger.info(f"Wrote output to {output}")

            return result

        finally:
            # Restore original factories
            if old_tool_factory:
                from .ir.factories import set_tool_factory

                set_tool_factory(old_tool_factory)
            if old_router_factory:
                from .ir.factories import set_router_factory

                set_router_factory(old_router_factory)


"""
Enrichment Strategy Interface for Fabric Integration.

Exposes Fabric's enrichment strategy interface for custom fragment composition.
This completes Tier 6 of the abstraction exposure analysis.

Enables:
- Custom merge logic
- Fragment composition strategies
- Conflict resolution
"""

from typing import Any, Dict, List, Optional

try:
    from universal_agent_fabric import (
        ComposableEnrichmentStrategy,
        DefaultEnrichmentStrategy,
        EnrichmentHandler,
        EnrichmentStrategy,
        NexusEnricher,
        RoleEnrichmentHandler,
        DomainEnrichmentHandler,
        PolicyEnrichmentHandler,
        MixinEnrichmentHandler,
    )
    FABRIC_AVAILABLE = True
except ImportError:
    FABRIC_AVAILABLE = False
    # Type stubs for when fabric is not available
    EnrichmentStrategy = None
    DefaultEnrichmentStrategy = None
    ComposableEnrichmentStrategy = None
    EnrichmentHandler = None
    NexusEnricher = None
    RoleEnrichmentHandler = None
    DomainEnrichmentHandler = None
    PolicyEnrichmentHandler = None
    MixinEnrichmentHandler = None


__all__ = [
    "EnrichmentStrategy",
    "DefaultEnrichmentStrategy",
    "ComposableEnrichmentStrategy",
    "EnrichmentHandler",
    "NexusEnricher",
    "RoleEnrichmentHandler",
    "DomainEnrichmentHandler",
    "PolicyEnrichmentHandler",
    "MixinEnrichmentHandler",
    "FABRIC_AVAILABLE",
]


def create_custom_enrichment_strategy(
    handlers: Optional[List[EnrichmentHandler]] = None,
) -> "ComposableEnrichmentStrategy":
    """
    Create a composable enrichment strategy with custom handlers.

    Args:
        handlers: List of custom enrichment handlers (optional)

    Returns:
        ComposableEnrichmentStrategy instance

    Example:
        from universal_agent_nexus.enrichment import (
            create_custom_enrichment_strategy,
            RoleEnrichmentHandler,
            CustomHandler,
        )

        strategy = create_custom_enrichment_strategy([
            RoleEnrichmentHandler(),
            CustomHandler(),
            PolicyEnrichmentHandler(),
        ])

        enricher = NexusEnricher(strategy=strategy)
        enriched = enricher.enrich(baseline_path, ...)
    """
    if not FABRIC_AVAILABLE:
        raise ImportError(
            "universal-agent-fabric>=0.2.0 is required for enrichment strategies. "
            "Install with: pip install universal-agent-fabric>=0.2.0"
        )

    strategy = ComposableEnrichmentStrategy()
    if handlers:
        for handler in handlers:
            strategy.add_handler(handler)
    return strategy


def create_default_enrichment_strategy() -> "DefaultEnrichmentStrategy":
    """
    Create the default enrichment strategy.

    Returns:
        DefaultEnrichmentStrategy instance
    """
    if not FABRIC_AVAILABLE:
        raise ImportError(
            "universal-agent-fabric>=0.2.0 is required for enrichment strategies. "
            "Install with: pip install universal-agent-fabric>=0.2.0"
        )

    return DefaultEnrichmentStrategy()


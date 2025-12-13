# Enrichment Strategy Example

This example demonstrates how to use custom enrichment strategies with Fabric v0.2.0+.

## Basic Usage

```python
from universal_agent_nexus.enrichment import (
    NexusEnricher,
    DefaultEnrichmentStrategy,
)

# Use default strategy
enricher = NexusEnricher(strategy=DefaultEnrichmentStrategy())
enriched = enricher.enrich(
    baseline_path="manifest.yaml",
    role_path="roles/researcher.yaml",
    domain_paths=["domains/finance.yaml"],
    policy_paths=["policies/safety.yaml"],
    output_path="enriched.yaml"
)
```

## Custom Enrichment Strategy

```python
from universal_agent_nexus.enrichment import (
    EnrichmentHandler,
    ComposableEnrichmentStrategy,
    NexusEnricher,
)

class CustomHandler(EnrichmentHandler):
    """Custom enrichment handler."""
    
    def handle(
        self,
        manifest: Dict[str, Any],
        role: Optional[Dict],
        domains: List[Dict],
        policies: List[Dict],
        mixins: List[Dict],
    ) -> Dict[str, Any]:
        """Add custom logic here."""
        # Example: Add custom metadata
        if "metadata" not in manifest:
            manifest["metadata"] = {}
        manifest["metadata"]["custom_field"] = "custom_value"
        return manifest

# Create composable strategy
strategy = ComposableEnrichmentStrategy()
strategy.add_handler(RoleEnrichmentHandler())
strategy.add_handler(CustomHandler())
strategy.add_handler(PolicyEnrichmentHandler())

# Use with enricher
enricher = NexusEnricher(strategy=strategy)
enriched = enricher.enrich(...)
```

## Using Convenience Function

```python
from universal_agent_nexus.enrichment import (
    create_custom_enrichment_strategy,
    RoleEnrichmentHandler,
    DomainEnrichmentHandler,
    PolicyEnrichmentHandler,
)

strategy = create_custom_enrichment_strategy([
    RoleEnrichmentHandler(),
    DomainEnrichmentHandler(),
    PolicyEnrichmentHandler(),
])

enricher = NexusEnricher(strategy=strategy)
```


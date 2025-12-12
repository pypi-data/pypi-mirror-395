"""
universal_agent_nexus.bridges

Schema translation bridges between Universal Agent libraries.

Bridges handle impedance mismatches between composition-time schemas
(Fabric) and runtime schemas (Architecture).
"""

from universal_agent_nexus.bridges.fabric_to_arch import (
    BridgeError,
    convert_governance_rule,
    convert_governance_rules,
    convert_fabric_spec_to_manifest,
)

__all__ = [
    "BridgeError",
    "convert_governance_rule",
    "convert_governance_rules",
    "convert_fabric_spec_to_manifest",
]


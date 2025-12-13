"""
universal_agent_nexus.bridges.fabric_to_arch

Bridge between Universal Agent Fabric (composition) and Universal Agent Architecture (runtime).

Converts:
- GovernanceRule → PolicyRule
- FabricSpec governance → PolicySpec
- (Future: Capability → ToolSpec, Domain → RouterSpec)
"""

from typing import List, Optional, TYPE_CHECKING
import logging

# universal-agent-fabric is now a required dependency
from universal_agent_fabric import GovernanceRule

FABRIC_AVAILABLE = True

try:
    from universal_agent.manifests.schema import PolicyRule, PolicySpec, PolicyAction
    ARCH_AVAILABLE = True
except ImportError:
    ARCH_AVAILABLE = False
    PolicyRule = None
    PolicySpec = None
    PolicyAction = None

if TYPE_CHECKING:
    from universal_agent_fabric import GovernanceRule, FabricSpec
    from universal_agent.manifests.schema import AgentManifest, PolicyRule, PolicySpec

logger = logging.getLogger(__name__)


class BridgeError(Exception):
    """Raised when schema conversion fails."""
    pass


def _check_dependencies():
    """Ensure required libraries are installed."""
    # universal-agent-fabric is now a required dependency, so FABRIC_AVAILABLE is always True
    if not ARCH_AVAILABLE:
        raise BridgeError(
            "universal-agent-arch not installed. "
            "Install with: pip install universal-agent-arch"
        )


def convert_governance_rule(rule: "GovernanceRule") -> "PolicyRule":
    """
    Convert a single Fabric GovernanceRule to Architecture PolicyRule.
    
    Args:
        rule: GovernanceRule from universal_agent_fabric
    
    Returns:
        PolicyRule compatible with universal_agent_architecture runtime
    
    Raises:
        BridgeError: If conversion fails or dependencies missing
    
    Example:
        >>> from universal_agent_fabric import GovernanceRule
        >>> fabric_rule = GovernanceRule(
        ...     name="no_violence",
        ...     target_pattern=".*violence.*",
        ...     action="deny"
        ... )
        >>> arch_rule = convert_governance_rule(fabric_rule)
        >>> assert arch_rule.action.value == "deny"
    """
    _check_dependencies()
    
    try:
        # Convert action string to enum (PolicyAction values are lowercase)
        action_str = rule.action.lower()
        if action_str not in ["allow", "deny", "require_approval"]:
            logger.warning(
                "Unknown action '%s' for rule '%s', defaulting to allow",
                rule.action, rule.name
            )
            action_str = "allow"
        
        # Convert target_pattern (regex) to target list
        # Architecture uses explicit target list, not regex
        target_list = [rule.target_pattern] if rule.target_pattern else ["*"]
        
        return PolicyRule(
            description=rule.name,
            target=target_list,
            action=PolicyAction(action_str),
            conditions=rule.conditions or {},
            approval_channel=None,  # Fabric doesn't have this concept
            metadata={"source": "fabric", "original_name": rule.name},
        )
    
    except Exception as e:
        raise BridgeError(f"Failed to convert rule '{rule.name}': {e}") from e


def convert_governance_rules(
    rules: List["GovernanceRule"],
    policy_name: str = "fabric_governance",
    policy_description: Optional[str] = None,
) -> "PolicySpec":
    """
    Convert a list of Fabric GovernanceRules to a single Architecture PolicySpec.
    
    Args:
        rules: List of GovernanceRule instances from Fabric
        policy_name: Name for the generated PolicySpec
        policy_description: Optional description for the PolicySpec
    
    Returns:
        PolicySpec containing all converted rules
    
    Raises:
        BridgeError: If conversion fails or dependencies missing
    
    Example:
        >>> rules = [
        ...     GovernanceRule(name="safety", action="deny", target_pattern="unsafe"),
        ...     GovernanceRule(name="approval", action="require_approval", target_pattern="critical")
        ... ]
        >>> policy_spec = convert_governance_rules(rules, policy_name="my_policies")
        >>> assert len(policy_spec.rules) == 2
    """
    _check_dependencies()
    
    if not rules:
        logger.warning("No governance rules to convert")
        return PolicySpec(
            name=policy_name,
            description=policy_description or "Empty policy spec from Fabric",
            rules=[],
        )
    
    converted_rules = []
    failed_rules = []
    
    for rule in rules:
        try:
            converted_rules.append(convert_governance_rule(rule))
        except BridgeError as e:
            logger.error("Failed to convert rule '%s': %s", rule.name, e)
            failed_rules.append(rule.name)
    
    if failed_rules:
        logger.warning(
            "Failed to convert %d/%d rules: %s",
            len(failed_rules), len(rules), failed_rules
        )
    
    return PolicySpec(
        name=policy_name,
        description=policy_description or f"Policies converted from Universal Agent Fabric ({len(converted_rules)} rules)",
        rules=converted_rules,
        metadata={
            "source": "fabric",
            "original_count": len(rules),
            "converted_count": len(converted_rules),
            "failed_count": len(failed_rules),
        }
    )


def convert_fabric_spec_to_manifest(
    fabric_spec: "FabricSpec",
    manifest: "AgentManifest",
) -> "AgentManifest":
    """
    Augment an AgentManifest with policies from a FabricSpec.
    
    This is the high-level bridge function used during compilation.
    
    Args:
        fabric_spec: FabricSpec from universal_agent_fabric
        manifest: Existing AgentManifest to augment
    
    Returns:
        Updated AgentManifest with Fabric governance converted to policies
    
    Example:
        >>> from universal_agent_fabric import FabricBuilder, FabricSpec
        >>> from universal_agent.manifests.schema import AgentManifest
        >>> 
        >>> # Build Fabric spec
        >>> fabric_spec = FabricBuilder(spec).build()
        >>> 
        >>> # Create base manifest
        >>> manifest = AgentManifest(name="my_agent", version="1.0.0")
        >>> 
        >>> # Bridge Fabric governance into manifest
        >>> manifest = convert_fabric_spec_to_manifest(fabric_spec, manifest)
        >>> 
        >>> # Now manifest.policies contains converted governance rules
        >>> assert any(p.name == "fabric_governance" for p in manifest.policies)
    """
    _check_dependencies()
    
    if not hasattr(fabric_spec, 'governance'):
        logger.info("FabricSpec has no governance attribute")
        return manifest
    
    governance_rules = fabric_spec.governance
    if not governance_rules:
        logger.info("FabricSpec has no governance rules")
        return manifest
    
    # Convert governance to PolicySpec
    policy_spec = convert_governance_rules(
        governance_rules,
        policy_name="fabric_governance",
        policy_description=f"Governance rules from {fabric_spec.name if hasattr(fabric_spec, 'name') else 'Fabric spec'}"
    )
    
    # Add to manifest
    manifest.policies.append(policy_spec)
    
    logger.info(
        "Converted %d Fabric governance rules to Architecture PolicySpec '%s'",
        len(policy_spec.rules), policy_spec.name
    )
    
    return manifest


__all__ = [
    "BridgeError",
    "convert_governance_rule",
    "convert_governance_rules",
    "convert_fabric_spec_to_manifest",
]


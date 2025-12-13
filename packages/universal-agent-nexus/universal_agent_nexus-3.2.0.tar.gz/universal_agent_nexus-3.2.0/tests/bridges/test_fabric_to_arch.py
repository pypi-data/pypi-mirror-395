"""
Tests for Fabric to Architecture bridge.
"""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


# Mock classes for when dependencies aren't installed
@dataclass
class MockGovernanceRule:
    """Mock GovernanceRule for testing."""
    name: str
    action: str
    target_pattern: str = "*"
    conditions: Optional[Dict[str, Any]] = None


@dataclass
class MockPolicyRule:
    """Mock PolicyRule for testing."""
    description: str
    target: List[str]
    action: Any
    conditions: Dict[str, Any]
    approval_channel: Optional[str]
    metadata: Dict[str, Any]


@dataclass
class MockPolicySpec:
    """Mock PolicySpec for testing."""
    name: str
    description: str
    rules: List[MockPolicyRule]
    metadata: Optional[Dict[str, Any]] = None


class MockPolicyAction:
    """Mock PolicyAction enum for testing."""
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    
    def __init__(self, value: str):
        self.value = value
    
    def __eq__(self, other):
        if isinstance(other, MockPolicyAction):
            return self.value == other.value
        return self.value == other


class TestBridgeImports:
    """Test bridge module imports."""

    def test_bridge_module_imports(self):
        """Test that bridge module can be imported."""
        from universal_agent_nexus.bridges import (
            BridgeError,
            convert_governance_rule,
            convert_governance_rules,
            convert_fabric_spec_to_manifest,
        )
        
        assert BridgeError is not None
        assert convert_governance_rule is not None
        assert convert_governance_rules is not None
        assert convert_fabric_spec_to_manifest is not None

    def test_bridge_error_is_exception(self):
        """Test BridgeError is a proper exception."""
        from universal_agent_nexus.bridges import BridgeError
        
        with pytest.raises(BridgeError):
            raise BridgeError("Test error")


class TestConvertGovernanceRule:
    """Tests for convert_governance_rule function."""

    @pytest.fixture
    def mock_dependencies(self):
        """Mock Fabric and Architecture dependencies."""
        with patch.dict('sys.modules', {
            'universal_agent_fabric': MagicMock(),
            'universal_agent': MagicMock(),
            'universal_agent.manifests': MagicMock(),
            'universal_agent.manifests.schema': MagicMock(),
        }):
            # Patch the module-level variables
            import universal_agent_nexus.bridges.fabric_to_arch as bridge_module
            
            original_fabric = bridge_module.FABRIC_AVAILABLE
            original_arch = bridge_module.ARCH_AVAILABLE
            original_policy_rule = bridge_module.PolicyRule
            original_policy_action = bridge_module.PolicyAction
            
            bridge_module.FABRIC_AVAILABLE = True
            bridge_module.ARCH_AVAILABLE = True
            bridge_module.PolicyRule = MockPolicyRule
            bridge_module.PolicyAction = MockPolicyAction
            
            yield bridge_module
            
            # Restore originals
            bridge_module.FABRIC_AVAILABLE = original_fabric
            bridge_module.ARCH_AVAILABLE = original_arch
            bridge_module.PolicyRule = original_policy_rule
            bridge_module.PolicyAction = original_policy_action

    def test_convert_deny_rule(self, mock_dependencies):
        """Test converting a deny rule."""
        bridge_module = mock_dependencies
        
        rule = MockGovernanceRule(
            name="no_violence",
            target_pattern=".*violence.*",
            action="deny",
        )
        
        policy_rule = bridge_module.convert_governance_rule(rule)
        
        assert policy_rule.description == "no_violence"
        assert policy_rule.action.value == "deny"
        assert ".*violence.*" in policy_rule.target
        assert policy_rule.metadata["source"] == "fabric"

    def test_convert_allow_rule(self, mock_dependencies):
        """Test converting an allow rule."""
        bridge_module = mock_dependencies
        
        rule = MockGovernanceRule(
            name="safe_content",
            target_pattern="safe_*",
            action="allow",
        )
        
        policy_rule = bridge_module.convert_governance_rule(rule)
        
        assert policy_rule.description == "safe_content"
        assert policy_rule.action.value == "allow"

    def test_convert_require_approval_rule(self, mock_dependencies):
        """Test converting a require_approval rule."""
        bridge_module = mock_dependencies
        
        rule = MockGovernanceRule(
            name="critical_ops",
            target_pattern="tool:delete_*",
            action="require_approval",
        )
        
        policy_rule = bridge_module.convert_governance_rule(rule)
        
        assert policy_rule.action.value == "require_approval"

    def test_unknown_action_defaults_to_allow(self, mock_dependencies):
        """Test that unknown actions default to allow."""
        bridge_module = mock_dependencies
        
        rule = MockGovernanceRule(
            name="unknown",
            target_pattern="*",
            action="weird_action",
        )
        
        policy_rule = bridge_module.convert_governance_rule(rule)
        
        assert policy_rule.action.value == "allow"


class TestConvertGovernanceRules:
    """Tests for convert_governance_rules function."""

    @pytest.fixture
    def mock_dependencies(self):
        """Mock Fabric and Architecture dependencies."""
        import universal_agent_nexus.bridges.fabric_to_arch as bridge_module
        
        original_fabric = bridge_module.FABRIC_AVAILABLE
        original_arch = bridge_module.ARCH_AVAILABLE
        original_policy_rule = bridge_module.PolicyRule
        original_policy_spec = bridge_module.PolicySpec
        original_policy_action = bridge_module.PolicyAction
        
        bridge_module.FABRIC_AVAILABLE = True
        bridge_module.ARCH_AVAILABLE = True
        bridge_module.PolicyRule = MockPolicyRule
        bridge_module.PolicySpec = MockPolicySpec
        bridge_module.PolicyAction = MockPolicyAction
        
        yield bridge_module
        
        # Restore originals
        bridge_module.FABRIC_AVAILABLE = original_fabric
        bridge_module.ARCH_AVAILABLE = original_arch
        bridge_module.PolicyRule = original_policy_rule
        bridge_module.PolicySpec = original_policy_spec
        bridge_module.PolicyAction = original_policy_action

    def test_convert_multiple_rules(self, mock_dependencies):
        """Test converting multiple rules."""
        bridge_module = mock_dependencies
        
        rules = [
            MockGovernanceRule(name="rule1", action="deny", target_pattern="bad"),
            MockGovernanceRule(name="rule2", action="allow", target_pattern="good"),
        ]
        
        policy_spec = bridge_module.convert_governance_rules(
            rules, 
            policy_name="test_policy"
        )
        
        assert policy_spec.name == "test_policy"
        assert len(policy_spec.rules) == 2
        assert policy_spec.rules[0].description == "rule1"
        assert policy_spec.rules[1].description == "rule2"

    def test_empty_rules_list(self, mock_dependencies):
        """Test converting empty rules list."""
        bridge_module = mock_dependencies
        
        policy_spec = bridge_module.convert_governance_rules(
            [], 
            policy_name="empty"
        )
        
        assert policy_spec.name == "empty"
        assert len(policy_spec.rules) == 0

    def test_custom_description(self, mock_dependencies):
        """Test custom policy description."""
        bridge_module = mock_dependencies
        
        rules = [
            MockGovernanceRule(name="rule1", action="deny", target_pattern="*"),
        ]
        
        policy_spec = bridge_module.convert_governance_rules(
            rules,
            policy_name="custom",
            policy_description="My custom description"
        )
        
        assert policy_spec.description == "My custom description"


class TestMissingDependencies:
    """Test behavior when dependencies are missing."""

    @pytest.mark.skip(reason="Fabric is now a required dependency, not optional")
    def test_missing_fabric_raises_bridge_error(self):
        """Test that missing Fabric raises BridgeError.
        
        NOTE: This test is skipped because universal-agent-fabric is now
        a required dependency (not optional), so _check_dependencies no
        longer validates FABRIC_AVAILABLE.
        """
        pass

    def test_missing_arch_raises_bridge_error(self):
        """Test that missing Architecture raises BridgeError."""
        import universal_agent_nexus.bridges.fabric_to_arch as bridge_module
        from universal_agent_nexus.bridges import BridgeError
        
        original_fabric = bridge_module.FABRIC_AVAILABLE
        original_arch = bridge_module.ARCH_AVAILABLE
        
        bridge_module.FABRIC_AVAILABLE = True
        bridge_module.ARCH_AVAILABLE = False
        
        try:
            with pytest.raises(BridgeError, match="universal-agent-arch not installed"):
                bridge_module._check_dependencies()
        finally:
            bridge_module.FABRIC_AVAILABLE = original_fabric
            bridge_module.ARCH_AVAILABLE = original_arch


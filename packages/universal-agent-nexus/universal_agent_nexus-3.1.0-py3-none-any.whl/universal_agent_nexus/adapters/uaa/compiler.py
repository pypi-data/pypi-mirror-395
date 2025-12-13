"""
UAA Native Generator - Compiles ManifestIR to UAA AgentManifest format.

This generator produces a UAA-native AgentManifest from the Nexus IR.
It's the simplest generator since the IR is already aligned with UAA's schema.

Usage:
    nexus compile agent.yaml --target uaa --output manifest.yaml
"""

from typing import Any, Dict, List, Optional
import yaml

try:
    from universal_agent.manifests.schema import (
        AgentManifest,
        GraphSpec,
        GraphNodeSpec,
        GraphEdgeSpec,
        EdgeCondition,
        ToolSpec,
        RouterSpec,
        PolicySpec,
        PolicyRule,
        GraphNodeKind,
        EdgeTrigger,
        ToolProtocol,
        RouterStrategyKind,
        PolicyAction,
        Metadata,
    )
    UAA_AVAILABLE = True
except ImportError:
    UAA_AVAILABLE = False


class UAANativeGenerator:
    """
    Generates a UAA-native AgentManifest from ManifestIR.
    
    This generator converts the Nexus Intermediate Representation directly
    into the UAA Kernel's AgentManifest format. Since the IR is designed
    to be compatible with UAA's schema, this is largely a serialization pass.
    """
    
    def __init__(self, validate: bool = True):
        """
        Initialize the UAA Native Generator.
        
        Args:
            validate: Whether to validate the output against UAA schema
        """
        self.validate = validate
        
        if not UAA_AVAILABLE:
            raise ImportError(
                "universal-agent-arch is required for UAA native generation. "
                "Install with: pip install universal-agent-arch"
            )
    
    def generate(self, ir: "ManifestIR") -> str:
        """
        Converts the ManifestIR into a UAA AgentManifest YAML string.
        
        Args:
            ir: The final, optimized Intermediate Representation
            
        Returns:
            A string containing the UAA-compliant AgentManifest in YAML format
        """
        manifest_dict = self._ir_to_manifest_dict(ir)
        
        if self.validate:
            # Validate by constructing the Pydantic model
            manifest = AgentManifest(**manifest_dict)
            manifest_dict = manifest.model_dump(exclude_none=True, mode="json")
        
        return yaml.dump(
            manifest_dict,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )
    
    def generate_manifest(self, ir: "ManifestIR") -> "AgentManifest":
        """
        Converts the ManifestIR into a UAA AgentManifest object.
        
        Args:
            ir: The final, optimized Intermediate Representation
            
        Returns:
            An AgentManifest Pydantic model instance
        """
        manifest_dict = self._ir_to_manifest_dict(ir)
        return AgentManifest(**manifest_dict)
    
    def _ir_to_manifest_dict(self, ir: "ManifestIR") -> Dict[str, Any]:
        """Convert IR to manifest dictionary."""
        return {
            "name": ir.name,
            "version": ir.version,
            "description": ir.description,
            "graphs": [self._convert_graph(g) for g in ir.graphs],
            "tools": [self._convert_tool(t) for t in ir.tools],
            "routers": [self._convert_router(r) for r in ir.routers],
            "policies": [self._convert_policy(p) for p in ir.policies],
            "metadata": self._convert_metadata(ir.metadata) if ir.metadata else None,
        }
    
    def _convert_graph(self, graph_ir: "GraphIR") -> Dict[str, Any]:
        """Convert GraphIR to GraphSpec dict."""
        return {
            "name": graph_ir.name,
            "version": getattr(graph_ir, "version", "1.0.0"),
            "description": getattr(graph_ir, "description", None),
            "entry_node": graph_ir.entry_node,
            "nodes": [self._convert_node(n) for n in graph_ir.nodes],
            "edges": [self._convert_edge(e) for e in graph_ir.edges],
            "metadata": self._convert_metadata(graph_ir.metadata) if hasattr(graph_ir, "metadata") else None,
        }
    
    def _convert_node(self, node_ir: "NodeIR") -> Dict[str, Any]:
        """Convert NodeIR to GraphNodeSpec dict."""
        node_dict = {
            "id": node_ir.id,
            "kind": self._map_node_kind(node_ir.kind),
            "label": getattr(node_ir, "label", None),
            "description": getattr(node_ir, "description", None),
        }
        
        # Add kind-specific references
        if hasattr(node_ir, "router_ref") and node_ir.router_ref:
            node_dict["router"] = {"name": node_ir.router_ref}
        
        if hasattr(node_ir, "tool_ref") and node_ir.tool_ref:
            node_dict["tool"] = {"name": node_ir.tool_ref}
        
        if hasattr(node_ir, "config") and node_ir.config:
            # Map config fields appropriately
            config = node_ir.config
            if "inputs" in config:
                node_dict["inputs"] = config["inputs"]
            if "output_map" in config:
                node_dict["output_map"] = config["output_map"]
            if "human_prompt" in config:
                node_dict["human_prompt"] = config["human_prompt"]
        
        # Handle annotations/metadata
        if hasattr(node_ir, "metadata") and node_ir.metadata:
            node_dict["metadata"] = self._convert_metadata(node_ir.metadata)
        
        return node_dict
    
    def _convert_edge(self, edge_ir: "EdgeIR") -> Dict[str, Any]:
        """Convert EdgeIR to GraphEdgeSpec dict."""
        edge_dict = {
            "from_node": edge_ir.from_node,
            "to_node": edge_ir.to_node,
        }
        
        # Convert condition
        if hasattr(edge_ir, "condition") and edge_ir.condition:
            condition = edge_ir.condition
            edge_dict["condition"] = {
                "trigger": self._map_trigger(condition.get("trigger", "success")),
                "expression": condition.get("expression"),
            }
        
        return edge_dict
    
    def _convert_tool(self, tool_ir: "ToolIR") -> Dict[str, Any]:
        """Convert ToolIR to ToolSpec dict."""
        return {
            "name": tool_ir.name,
            "description": getattr(tool_ir, "description", None),
            "protocol": self._map_protocol(tool_ir.protocol),
            "config": tool_ir.config if hasattr(tool_ir, "config") else {},
            "tags": getattr(tool_ir, "tags", []),
        }
    
    def _convert_router(self, router_ir: "RouterIR") -> Dict[str, Any]:
        """Convert RouterIR to RouterSpec dict."""
        return {
            "name": router_ir.name,
            "description": getattr(router_ir, "description", None),
            "strategy": self._map_router_strategy(router_ir.strategy),
            "system_message": router_ir.system_message,
            "model_candidates": getattr(router_ir, "model_candidates", []),
            "default_model": getattr(router_ir, "default_model", None),
        }
    
    def _convert_policy(self, policy_ir: "PolicyIR") -> Dict[str, Any]:
        """Convert PolicyIR to PolicySpec dict."""
        return {
            "name": policy_ir.name,
            "description": getattr(policy_ir, "description", None),
            "rules": [self._convert_policy_rule(r) for r in policy_ir.rules],
        }
    
    def _convert_policy_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Convert policy rule dict."""
        return {
            "description": rule.get("description", rule.get("name")),
            "target": rule.get("target", [rule.get("target_pattern", "*")]),
            "action": self._map_policy_action(rule.get("action", "allow")),
            "conditions": rule.get("conditions", {}),
        }
    
    def _convert_metadata(self, metadata: Any) -> Optional[Dict[str, Any]]:
        """Convert metadata to dict."""
        if metadata is None:
            return None
        if isinstance(metadata, dict):
            return {
                "tags": metadata.get("tags", []),
                "extra": metadata.get("extra", metadata),
            }
        if hasattr(metadata, "model_dump"):
            return metadata.model_dump()
        return {"extra": metadata}
    
    def _map_node_kind(self, kind: Any) -> str:
        """Map IR node kind to UAA GraphNodeKind."""
        kind_str = str(kind).lower() if kind else "task"
        
        # Handle enum values
        if hasattr(kind, "value"):
            kind_str = kind.value.lower()
        
        mapping = {
            "task": "task",
            "router": "router",
            "tool": "tool",
            "subgraph": "subgraph",
            "human": "human",
        }
        return mapping.get(kind_str, "task")
    
    def _map_trigger(self, trigger: Any) -> str:
        """Map IR trigger to UAA EdgeTrigger."""
        trigger_str = str(trigger).lower() if trigger else "success"
        
        if hasattr(trigger, "value"):
            trigger_str = trigger.value.lower()
        
        mapping = {
            "success": "success",
            "error": "error",
            "timeout": "timeout",
            "approval": "approval",
            "rejection": "rejection",
            "custom": "custom",
        }
        return mapping.get(trigger_str, "success")
    
    def _map_protocol(self, protocol: Any) -> str:
        """Map IR protocol to UAA ToolProtocol."""
        protocol_str = str(protocol).lower() if protocol else "local"
        
        if hasattr(protocol, "value"):
            protocol_str = protocol.value.lower()
        
        mapping = {
            "mcp": "mcp",
            "http": "http",
            "subprocess": "subprocess",
            "local": "local",
        }
        return mapping.get(protocol_str, "local")
    
    def _map_router_strategy(self, strategy: Any) -> str:
        """Map IR router strategy to UAA RouterStrategyKind."""
        strategy_str = str(strategy).lower() if strategy else "llm"
        
        if hasattr(strategy, "value"):
            strategy_str = strategy.value.lower()
        
        mapping = {
            "rule": "rule",
            "llm": "llm",
            "hybrid": "hybrid",
        }
        return mapping.get(strategy_str, "llm")
    
    def _map_policy_action(self, action: Any) -> str:
        """Map IR policy action to UAA PolicyAction."""
        action_str = str(action).lower() if action else "allow"
        
        if hasattr(action, "value"):
            action_str = action.value.lower()
        
        mapping = {
            "allow": "allow",
            "deny": "deny",
            "require_approval": "require_approval",
        }
        return mapping.get(action_str, "allow")


__all__ = ["UAANativeGenerator"]


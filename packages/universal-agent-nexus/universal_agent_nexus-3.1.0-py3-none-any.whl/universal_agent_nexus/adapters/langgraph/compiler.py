"""
universal_agent_nexus.adapters.langgraph.compiler

Compiles UAA manifests to LangGraph StateGraph.

Philosophy: Let LangGraph handle routing, tools, state.
We handle ONLY: YAML → LangGraph translation.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

try:
    from langgraph.graph import END, StateGraph
    from langgraph.graph.message import MessagesState
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Install 'universal-agent-nexus[langgraph]' to use this adapter."
    ) from exc

from universal_agent.manifests.schema import AgentManifest, EdgeTrigger, GraphNodeKind
from universal_agent_nexus.adapters.base import BaseCompiler
from universal_agent_nexus.adapters.langgraph.factory import LLMFactory

logger = logging.getLogger(__name__)


class LangGraphCompiler(BaseCompiler):
    """
    Compile UAA manifests to LangGraph StateGraph.
    
    Design principle: Minimal wrapper. Let LangGraph do the heavy lifting.
    """

    def __init__(self, mcp_config: Optional[Dict[str, Any]] = None):
        self.mcp_config = mcp_config or {}
        self._manifest: Optional[AgentManifest] = None

    def compile(self, manifest: AgentManifest, graph_name: str) -> StateGraph:
        """Compile manifest graph to LangGraph StateGraph."""
        self._manifest = manifest
        graph_spec = next((g for g in manifest.graphs if g.name == graph_name), None)
        if not graph_spec:
            raise ValueError(f"Graph '{graph_name}' not found in manifest.")

        # Use LangGraph's MessagesState - battle-tested, standard
        workflow = StateGraph(MessagesState)

        # 1. Add nodes - minimal wrappers
        for node in graph_spec.nodes:
            if node.kind == GraphNodeKind.ROUTER:
                workflow.add_node(node.id, self._create_router_node(node))
            else:
                workflow.add_node(node.id, self._create_passthrough_node(node.id))

        # 2. Build edges - let LangGraph handle routing
        edges_by_source: Dict[str, List] = defaultdict(list)
        for edge in graph_spec.edges:
            edges_by_source[edge.from_node].append(edge)

        for from_node, edges in edges_by_source.items():
            if len(edges) == 1 and not self._has_conditions(edges[0]):
                # Simple edge - LangGraph handles it
                workflow.add_edge(from_node, edges[0].to_node)
            else:
                # Conditional routing - build path map, let LangGraph route
                path_map = self._build_path_map(edges)
                routing_fn = self._create_router(edges)
                workflow.add_conditional_edges(from_node, routing_fn, path_map)

        # 3. Entry point and terminals
        workflow.set_entry_point(graph_spec.entry_node)
        all_nodes = {n.id for n in graph_spec.nodes}
        nodes_with_edges = set(edges_by_source.keys())
        for terminal in (all_nodes - nodes_with_edges):
            workflow.add_edge(terminal, END)

        return workflow

    def _create_router_node(self, node_spec):
        """Create router node - invokes LLM, stores response for routing."""
        async def router_fn(state: MessagesState) -> MessagesState:
            node_id = getattr(node_spec, "id", "router")
            
            # Get LLM config from manifest
            llm, system_msg = self._get_llm_config(node_spec)
            if not llm:
                logger.warning("Router '%s' has no LLM config", node_id)
                return state

            # Build messages - LangGraph's MessagesState handles history
            messages = list(state.get("messages", []))
            if system_msg and (not messages or not isinstance(messages[0], SystemMessage)):
                messages.insert(0, SystemMessage(content=system_msg))

            try:
                response = await llm.ainvoke(messages)
                logger.info("Router %s: %s", node_id, str(response.content)[:80])
                return {"messages": [response]}
            except Exception as e:
                logger.exception("Router %s failed: %s", node_id, e)
                return {"messages": [AIMessage(content=f"error: {e}")]}

        return router_fn

    def _create_passthrough_node(self, node_id: str):
        """Passthrough node - just logs execution."""
        async def passthrough_fn(state: MessagesState) -> MessagesState:
            logger.info("Executing node: %s", node_id)
            return state
        return passthrough_fn

    def _get_llm_config(self, node_spec):
        """Extract LLM and system message from node/manifest."""
        router_ref = getattr(node_spec, "router_ref", None) or getattr(node_spec, "router", None)
        
        if router_ref and self._manifest:
            router_name = getattr(router_ref, "name", router_ref) if hasattr(router_ref, "name") else router_ref
            routers = getattr(self._manifest, "routers", []) or []
            router_spec = next((r for r in routers if r.name == router_name), None)
            
            if router_spec:
                model = getattr(router_spec, "default_model", None) or (
                    getattr(router_spec, "model_candidates", [None]) or [None]
                )[0]
                if model:
                    config = getattr(router_spec, "config", {}) or {}
                    llm_config = {"temperature": config.get("temperature", 0.2)}
                    if config.get("base_url"):
                        llm_config["base_url"] = config["base_url"]
                    if config.get("api_key"):
                        llm_config["api_key"] = config["api_key"]
                    
                    try:
                        llm = LLMFactory.create(model, llm_config)
                        return llm, getattr(router_spec, "system_message", None)
                    except Exception as e:
                        logger.error("Failed to create LLM: %s", e)
        
        return None, None

    def _build_path_map(self, edges: List) -> Dict[str, str]:
        """Build path map for conditional edges."""
        path_map = {END: END}
        for edge in edges:
            path_map[edge.to_node] = edge.to_node
            # Add route keys as paths too
            cond = getattr(edge, "condition", None)
            if cond and getattr(cond, "route", None):
                path_map[cond.route] = edge.to_node
        return path_map

    def _create_router(self, edges: List) -> Callable:
        """Create routing function - minimal logic, let LangGraph call it."""
        def route(state: MessagesState) -> str:
            messages = state.get("messages", [])
            last_msg = messages[-1] if messages else None
            last_response = getattr(last_msg, "content", "") if last_msg else ""
            last_lower = str(last_response).lower().strip()

            # Check for errors first
            if last_lower.startswith("error:"):
                for edge in edges:
                    cond = getattr(edge, "condition", None)
                    if cond and getattr(cond, "trigger", None) == EdgeTrigger.ERROR:
                        return edge.to_node
                return END

            # Match route keys against response
            for edge in edges:
                cond = getattr(edge, "condition", None)
                if not cond:
                    continue
                    
                route_key = getattr(cond, "route", None)
                if route_key and route_key.lower() in last_lower:
                    logger.debug("Route matched: %s -> %s", route_key, edge.to_node)
                    return edge.to_node

            # Default: first edge or END
            return edges[0].to_node if edges else END

        return route

    @staticmethod
    def _has_conditions(edge) -> bool:
        """Check if edge has routing conditions."""
        cond = getattr(edge, "condition", None)
        if not cond:
            return False
        return bool(
            getattr(cond, "expression", None) or
            getattr(cond, "route", None) or
            getattr(cond, "trigger", None) == EdgeTrigger.ERROR
        )

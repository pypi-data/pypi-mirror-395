"""
universal_agent_nexus.adapters.langgraph.compiler

Compiles a UAA GraphSpec into a LangGraph StateGraph using MCP tools.

Security: Uses simpleeval for safe expression evaluation (no eval() RCE risk).
"""

from __future__ import annotations

import asyncio
import logging
import operator
from collections import defaultdict
from functools import partial
from typing import Annotated, Any, Callable, Dict, List, Optional, TypedDict

try:
    from langgraph.graph import END, START, StateGraph
    from langchain_core.messages import BaseMessage, HumanMessage
    from langchain_mcp_adapters.client import MultiServerMCPClient
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "Install 'universal-agent-nexus[langgraph]' to use this adapter."
    ) from exc

# Safe expression evaluation - no eval() RCE vulnerability
from simpleeval import SimpleEval, NameNotDefined

from universal_agent.manifests.schema import (
    AgentManifest,
    EdgeTrigger,
    GraphNodeKind,
)
from universal_agent_nexus.adapters.base import BaseCompiler

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """LangGraph state compatible with UAA."""

    context: Dict[str, Any]
    history: Annotated[list[BaseMessage], operator.add]
    current_node: str
    error: Optional[str]


class LangGraphCompiler(BaseCompiler):
    """Compile UAA manifests to LangGraph StateGraph."""

    def __init__(self, mcp_config: Optional[Dict[str, Any]] = None):
        self.mcp_config = mcp_config or {}
        self._manifest: Optional[AgentManifest] = None

    def compile(self, manifest: AgentManifest, graph_name: str) -> StateGraph:
        """Synchronous wrapper around async compilation."""
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._compile_async(manifest, graph_name))

        # If already in an event loop, run in a task and wait.
        return asyncio.get_event_loop().run_until_complete(
            self._compile_async(manifest, graph_name)
        )

    async def compile_async(
        self, manifest: AgentManifest, graph_name: str
    ) -> StateGraph:
        """Async-friendly compilation entrypoint."""
        return await self._compile_async(manifest, graph_name)

    async def _compile_async(
        self, manifest: AgentManifest, graph_name: str
    ) -> StateGraph:
        self._manifest = manifest
        graph_spec = next((g for g in manifest.graphs if g.name == graph_name), None)
        if not graph_spec:
            raise ValueError(f"Graph '{graph_name}' not found in manifest.")

        # Only initialize MCP client if there are MCP tools configured
        mcp_config = self.mcp_config or self._build_mcp_config_from_manifest(manifest)
        tools: list = []
        if mcp_config:
            try:
                mcp_client = MultiServerMCPClient(mcp_config)
                tools = await mcp_client.get_tools()
            except Exception as e:
                logger.warning("MCP client init failed: %s", e)
        tool_index = {getattr(t, "name", ""): t for t in tools}

        workflow = StateGraph(AgentState)

        # 1. Add Nodes
        for node in graph_spec.nodes:
            if node.kind == GraphNodeKind.ROUTER:
                workflow.add_node(node.id, self._create_router_node(node))
            elif node.kind == GraphNodeKind.TOOL:
                workflow.add_node(node.id, self._create_tool_node(node, tool_index))
            else:
                workflow.add_node(node.id, self._create_task_node(node))

        # 2. Process Edges - Group by source for proper routing
        edges_by_source: Dict[str, List] = defaultdict(list)
        for edge in graph_spec.edges:
            edges_by_source[edge.from_node].append(edge)

        # Process each source node's outgoing edges
        for from_node, edges in edges_by_source.items():
            path_map = {edge.to_node: edge.to_node for edge in edges}
            path_map[END] = END

            if self._requires_routing(edges):
                # Complex case: Multiple edges OR conditional logic
                routing_fn = self._create_routing_function(edges)
                workflow.add_conditional_edges(from_node, routing_fn, path_map)
            else:
                # Simple case: Single, unconditional success edge
                edge = edges[0]
                workflow.add_edge(from_node, edge.to_node)

        # 3. Set entry point and handle terminals
        workflow.set_entry_point(graph_spec.entry_node)
        nodes_with_outgoing = set(edges_by_source.keys())
        all_node_ids = {n.id for n in graph_spec.nodes}
        terminal_nodes = all_node_ids - nodes_with_outgoing
        for terminal in terminal_nodes:
            workflow.add_edge(terminal, END)

        return workflow

    @staticmethod
    def _requires_routing(edges: List) -> bool:
        """
        Topology-based detection: determine if dynamic routing is needed.
        
        Uses graph structure rather than node labels to decide routing.
        Any node with multiple outgoing edges or conditional logic needs routing.
        """
        if len(edges) > 1:
            return True
        
        # Even a single edge needs routing if it has conditions
        edge = edges[0]
        condition = getattr(edge, "condition", None)
        if not condition:
            return False
            
        return bool(
            getattr(condition, "expression", None) or
            getattr(condition, "route", None) or
            getattr(condition, "trigger", None) == EdgeTrigger.ERROR
        )

    def _build_mcp_config_from_manifest(self, manifest: AgentManifest) -> Dict[str, Any]:
        """Translate manifest tool definitions into MCP server config."""
        mcp_servers: Dict[str, Any] = {}
        tools = getattr(manifest, "tools", []) or []
        for tool in tools:
            protocol = getattr(tool, "protocol", None)
            if protocol == "mcp":
                name = getattr(tool, "name", "tool")
                config = getattr(tool, "config", {}) or {}
                mcp_servers[name] = {
                    "transport": getattr(tool, "transport", None)
                    or config.get("transport", "stdio"),
                    "command": getattr(tool, "command", None) or config.get("command"),
                    "args": getattr(tool, "args", None) or config.get("args", []),
                }
        return mcp_servers

    def _create_router_node(self, node_spec):
        async def router_fn(state: AgentState) -> AgentState:
            node_id = getattr(node_spec, "id", "router")
            logger.info("Routing at node %s", node_id)
            router_ref = getattr(node_spec, "router", None)
            if not router_ref or not self._manifest:
                return {**state, "current_node": node_id}

            routers = getattr(self._manifest, "routers", []) or []
            router_spec = next(
                (r for r in routers if getattr(r, "name", None) == router_ref.name),
                None,
            )
            if not router_spec:
                logger.warning("Router %s not found in manifest", router_ref.name)
                return {**state, "current_node": node_id}

            model = getattr(router_spec, "default_model", None) or (
                getattr(router_spec, "model_candidates", []) or [None]
            )[0]
            if not model:
                logger.warning("Router %s missing model configuration", router_ref.name)
                return {**state, "current_node": node_id}

            try:
                from langchain_openai import ChatOpenAI
            except ImportError as exc:  # pragma: no cover - optional dependency
                raise ImportError(
                    "Install langchain-openai to use router LLM nodes."
                ) from exc

            llm = ChatOpenAI(model=model, temperature=0.2)
            messages = state.get("history", [])
            if not messages and state.get("context", {}).get("query"):
                messages = [HumanMessage(content=state["context"]["query"])]

            system_message = getattr(router_spec, "system_message", None)
            if system_message:
                from langchain_core.messages import SystemMessage

                messages = [SystemMessage(content=system_message), *messages]

            try:
                response = await llm.ainvoke(messages)
                logger.info("Router %s response: %s", node_id, str(response)[:120])
                return {
                    **state,
                    "current_node": node_id,
                    "history": [*messages, response],
                    "context": {
                        **state.get("context", {}),
                        "last_response": getattr(response, "content", None),
                    },
                }
            except Exception as exc:  # pragma: no cover - runtime path
                logger.exception("Router %s failed", node_id)
                return {**state, "current_node": node_id, "error": str(exc)}

        return router_fn

    def _create_task_node(self, node_spec):
        async def task_fn(state: AgentState) -> AgentState:
            node_id = getattr(node_spec, "id", "task")
            logger.info("Executing task node %s", node_id)
            return {**state, "current_node": node_id}

        return task_fn

    def _create_tool_node(self, node_spec, tools: Dict[str, Any]):
        async def tool_fn(state: AgentState) -> AgentState:
            node_id = getattr(node_spec, "id", "tool")
            logger.info("Executing tool node %s", node_id)
            tool_ref = getattr(node_spec, "tool", None)
            tool_name = getattr(tool_ref, "name", node_id) if tool_ref else node_id
            tool = tools.get(tool_name)
            try:
                if tool and hasattr(tool, "ainvoke"):
                    tool_input = state.get("context", {}).get("tool_input", {})
                    result = await tool.ainvoke(tool_input)
                    new_context = {
                        **state.get("context", {}),
                        "tool_result": result,
                    }
                    return {**state, "context": new_context, "current_node": node_id}
            except Exception as exc:  # pragma: no cover - runtime path
                logger.exception("Tool node %s failed", node_id)
                return {**state, "current_node": node_id, "error": str(exc)}
            return {**state, "current_node": node_id}

        return tool_fn

    @staticmethod
    def _route_on_error(state: AgentState, target: str):
        return target if state.get("error") else END

    def _create_routing_function(self, edges: List) -> Callable[[AgentState], str]:
        """
        Create a routing function using Chain of Responsibility pattern.
        
        Priority order:
        1. Error handlers (if state has error)
        2. Expression conditions (evaluated safely)
        3. Route key matching (string/semantic match)
        4. Unconditional/default edges
        5. Fallback to END
        """
        def routing_fn(state: AgentState) -> str:
            context = state.get("context", {})
            last_response = context.get("last_response", "")
            error = state.get("error")
            current_node = state.get("current_node", "unknown")

            # Priority 1: Error Handling
            # If state has error, ONLY consider error triggers
            if error:
                for edge in edges:
                    cond = getattr(edge, "condition", None)
                    if cond and getattr(cond, "trigger", None) == EdgeTrigger.ERROR:
                        logger.info(
                            "Routing error from %s to %s", current_node, edge.to_node
                        )
                        return edge.to_node
                # No error handler found, terminate
                logger.warning(
                    "Error in %s but no error handler, falling back to END", current_node
                )
                return END

            # Priority 2: Evaluate conditions in order
            for edge in edges:
                cond = getattr(edge, "condition", None)

                # Unconditional edge acts as default if reached
                if not cond:
                    return edge.to_node

                trigger = getattr(cond, "trigger", EdgeTrigger.SUCCESS)
                if trigger == EdgeTrigger.ERROR:
                    continue  # Skip error handlers in normal flow

                # A. Check Expression condition
                expression = getattr(cond, "expression", None)
                if expression:
                    if self._evaluate_expression_safe(expression, context):
                        logger.debug(
                            "Expression '%s' matched, routing to %s",
                            expression, edge.to_node
                        )
                        return edge.to_node
                    continue  # Condition failed, try next edge

                # B. Check Route key (string/semantic match)
                route_key = getattr(cond, "route", None)
                if route_key:
                    if self._evaluate_route_match(route_key, last_response):
                        logger.debug(
                            "Route '%s' matched, routing to %s",
                            route_key, edge.to_node
                        )
                        return edge.to_node
                    continue  # Route didn't match, try next edge

                # C. Explicit SUCCESS trigger with no other criteria = pass-through
                if trigger == EdgeTrigger.SUCCESS:
                    return edge.to_node

            # Fallback: no conditions matched
            logger.warning(
                "No valid route found from %s, falling back to END", current_node
            )
            return END

        return routing_fn

    @staticmethod
    def _evaluate_expression_safe(expression: str, context: Dict[str, Any]) -> bool:
        """
        Safely evaluate expressions using simpleeval (no eval() RCE risk).
        
        Supports expressions like:
        - "risk_level > 0.5"
        - "category == 'spam'"
        - "confidence >= 0.8 and risk_level < 0.3"
        """
        evaluator = SimpleEval(
            names=context,
            functions={
                "len": len,
                "min": min,
                "max": max,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "abs": abs,
            }
        )
        try:
            result = evaluator.eval(expression)
            return bool(result)
        except NameNotDefined as e:
            logger.debug("Expression '%s' has undefined name: %s", expression, e)
            return False
        except SyntaxError as e:
            logger.warning("Expression '%s' has syntax error: %s", expression, e)
            return False
        except Exception as e:
            logger.debug("Expression '%s' evaluation failed: %s", expression, e)
            return False

    @staticmethod
    def _evaluate_route_match(route_key: str, last_response: Any) -> bool:
        """
        Evaluate string matching for route keys.
        
        Matches if the route key appears in or equals the response.
        Can be upgraded to regex or fuzzy matching in the future.
        """
        if not last_response:
            return False

        r_key = route_key.lower().strip()
        r_resp = str(last_response).lower().strip()

        # Exact match OR substring match
        return r_key in r_resp or r_key == r_resp

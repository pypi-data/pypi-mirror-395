"""
universal_agent_nexus.adapters.langgraph.compiler

Compiles a UAA GraphSpec into a LangGraph StateGraph using MCP tools.
"""

from __future__ import annotations

import asyncio
import logging
import operator
from functools import partial
from typing import Annotated, Any, Dict, Optional, TypedDict, cast

try:
    from langgraph.graph import END, START, StateGraph
    from langchain_core.messages import BaseMessage, HumanMessage
    from langchain_mcp_adapters.client import MultiServerMCPClient
except ImportError as exc:  # pragma: no cover - optional dependency
    raise ImportError(
        "Install 'universal-agent-nexus[langgraph]' to use this adapter."
    ) from exc

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

        for node in graph_spec.nodes:
            if node.kind == GraphNodeKind.ROUTER:
                workflow.add_node(node.id, self._create_router_node(node))
            elif node.kind == GraphNodeKind.TOOL:
                workflow.add_node(node.id, self._create_tool_node(node, tool_index))
            else:
                workflow.add_node(node.id, self._create_task_node(node))

        for edge in graph_spec.edges:
            trigger = edge.condition.trigger if edge.condition else EdgeTrigger.SUCCESS
            if trigger == EdgeTrigger.SUCCESS:
                workflow.add_edge(edge.from_node, edge.to_node)
            elif trigger == EdgeTrigger.ERROR:
                workflow.add_conditional_edges(
                    edge.from_node,
                    partial(self._route_on_error, target=edge.to_node),
                )

        workflow.set_entry_point(graph_spec.entry_node)
        # Find terminal nodes (nodes with no outgoing edges) and connect them to END
        nodes_with_outgoing = {e.from_node for e in graph_spec.edges}
        all_node_ids = {n.id for n in graph_spec.nodes}
        terminal_nodes = all_node_ids - nodes_with_outgoing
        for terminal in terminal_nodes:
            workflow.add_edge(terminal, END)
        return workflow

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


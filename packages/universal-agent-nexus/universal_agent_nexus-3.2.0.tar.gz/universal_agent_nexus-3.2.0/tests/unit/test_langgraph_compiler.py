"""
Tests for LangGraph compiler (v3.0.0+).

Tests the simplified compiler that uses LangGraph's native patterns:
- MessagesState instead of custom AgentState
- Minimal routing logic
- Let LangGraph do the heavy lifting
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

# Skip all tests if langgraph not installed
pytest.importorskip("langgraph", reason="LangGraph not installed")

# Import compiler (only after skip check)
from universal_agent_nexus.adapters.langgraph.compiler import LangGraphCompiler


class TestLangGraphCompilerBasics:
    """Test basic compiler functionality."""

    def test_compiler_init(self):
        """Test compiler initialization."""
        compiler = LangGraphCompiler()
        assert compiler.mcp_config == {}
        assert compiler._manifest is None

    def test_compiler_init_with_mcp_config(self):
        """Test compiler initialization with MCP config."""
        mcp_config = {"server": {"command": "mcp-server"}}
        compiler = LangGraphCompiler(mcp_config=mcp_config)
        assert compiler.mcp_config == mcp_config

    def test_compile_missing_graph(self):
        """Test compile raises error for missing graph."""
        compiler = LangGraphCompiler()
        manifest = Mock()
        manifest.graphs = []

        with pytest.raises(ValueError, match="not found"):
            compiler.compile(manifest, "nonexistent")

    def test_compile_simple_graph(self):
        """Test compiling a simple graph with one node."""
        compiler = LangGraphCompiler()

        # Create mock manifest
        node = Mock()
        node.id = "start"
        node.kind = Mock()
        node.kind.name = "TASK"
        node.kind.value = "task"

        graph = Mock()
        graph.name = "main"
        graph.nodes = [node]
        graph.edges = []
        graph.entry_node = "start"

        manifest = Mock()
        manifest.graphs = [graph]
        manifest.routers = []

        # Mock GraphNodeKind comparison
        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.GraphNodeKind"
        ) as mock_kind:
            mock_kind.ROUTER = Mock()
            node.kind = Mock()  # Not ROUTER

            state_graph = compiler.compile(manifest, "main")

        # Should return a StateGraph
        assert state_graph is not None

    def test_compile_with_edges(self):
        """Test compiling graph with simple edges."""
        compiler = LangGraphCompiler()

        # Create mock nodes
        node_a = Mock()
        node_a.id = "a"
        node_a.kind = Mock()

        node_b = Mock()
        node_b.id = "b"
        node_b.kind = Mock()

        # Create mock edge
        edge = Mock()
        edge.from_node = "a"
        edge.to_node = "b"
        edge.condition = None

        graph = Mock()
        graph.name = "main"
        graph.nodes = [node_a, node_b]
        graph.edges = [edge]
        graph.entry_node = "a"

        manifest = Mock()
        manifest.graphs = [graph]
        manifest.routers = []

        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.GraphNodeKind"
        ) as mock_kind:
            mock_kind.ROUTER = Mock()

            state_graph = compiler.compile(manifest, "main")

        assert state_graph is not None


class TestPathMapBuilding:
    """Test path map construction for conditional edges."""

    def test_build_path_map_simple(self):
        """Test building path map from edges."""
        compiler = LangGraphCompiler()

        edge1 = Mock()
        edge1.to_node = "node_a"
        edge1.condition = None

        edge2 = Mock()
        edge2.to_node = "node_b"
        edge2.condition = None

        path_map = compiler._build_path_map([edge1, edge2])

        assert "node_a" in path_map
        assert "node_b" in path_map
        assert "__end__" in path_map  # END is always included

    def test_build_path_map_with_route_keys(self):
        """Test path map includes route keys."""
        compiler = LangGraphCompiler()

        condition = Mock()
        condition.route = "safe"

        edge = Mock()
        edge.to_node = "approve"
        edge.condition = condition

        path_map = compiler._build_path_map([edge])

        assert "approve" in path_map
        assert "safe" in path_map  # Route key should map to target


class TestRouterCreation:
    """Test router node creation and routing logic."""

    def test_create_router_returns_function(self):
        """Test _create_router returns a callable."""
        compiler = LangGraphCompiler()

        edge = Mock()
        edge.to_node = "next"
        edge.condition = None

        router_fn = compiler._create_router([edge])

        assert callable(router_fn)

    def test_router_matches_route_key(self):
        """Test router matches route key in response."""
        compiler = LangGraphCompiler()

        # Create edges with route conditions
        cond_safe = Mock()
        cond_safe.route = "safe"
        cond_safe.trigger = Mock()
        cond_safe.trigger.value = "success"

        edge_safe = Mock()
        edge_safe.to_node = "approve"
        edge_safe.condition = cond_safe

        cond_risky = Mock()
        cond_risky.route = "risky"
        cond_risky.trigger = Mock()
        cond_risky.trigger.value = "success"

        edge_risky = Mock()
        edge_risky.to_node = "reject"
        edge_risky.condition = cond_risky

        router_fn = compiler._create_router([edge_safe, edge_risky])

        # Test routing with "safe" response
        state_safe = {"messages": [Mock(content="The content is safe")]}
        result = router_fn(state_safe)
        assert result == "approve"

        # Test routing with "risky" response
        state_risky = {"messages": [Mock(content="This is risky content")]}
        result = router_fn(state_risky)
        assert result == "reject"

    def test_router_handles_empty_messages(self):
        """Test router handles state with no messages."""
        compiler = LangGraphCompiler()

        edge = Mock()
        edge.to_node = "default"
        edge.condition = None

        router_fn = compiler._create_router([edge])

        state = {"messages": []}
        result = router_fn(state)
        assert result == "default"

    def test_router_handles_error_response(self):
        """Test router detects error responses."""
        compiler = LangGraphCompiler()

        # Create error handler edge
        from universal_agent_nexus.adapters.langgraph.compiler import EdgeTrigger

        cond_error = Mock()
        cond_error.trigger = EdgeTrigger.ERROR
        cond_error.route = None

        edge_error = Mock()
        edge_error.to_node = "error_handler"
        edge_error.condition = cond_error

        edge_normal = Mock()
        edge_normal.to_node = "normal"
        edge_normal.condition = None

        router_fn = compiler._create_router([edge_error, edge_normal])

        # Test with error response
        state = {"messages": [Mock(content="error: something went wrong")]}
        result = router_fn(state)
        assert result == "error_handler"


class TestConditionDetection:
    """Test edge condition detection."""

    def test_has_conditions_false_for_none(self):
        """Test _has_conditions returns False for no condition."""
        edge = Mock()
        edge.condition = None

        result = LangGraphCompiler._has_conditions(edge)
        assert result is False

    def test_has_conditions_true_for_expression(self):
        """Test _has_conditions detects expression."""
        condition = Mock()
        condition.expression = "x > 5"
        condition.route = None
        condition.trigger = Mock()
        condition.trigger.value = "success"

        edge = Mock()
        edge.condition = condition

        # Mock EdgeTrigger.ERROR
        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.EdgeTrigger"
        ) as mock_trigger:
            mock_trigger.ERROR = Mock()
            result = LangGraphCompiler._has_conditions(edge)

        assert result is True

    def test_has_conditions_true_for_route(self):
        """Test _has_conditions detects route key."""
        condition = Mock()
        condition.expression = None
        condition.route = "safe"
        condition.trigger = Mock()
        condition.trigger.value = "success"

        edge = Mock()
        edge.condition = condition

        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.EdgeTrigger"
        ) as mock_trigger:
            mock_trigger.ERROR = Mock()
            result = LangGraphCompiler._has_conditions(edge)

        assert result is True


class TestLLMConfigExtraction:
    """Test LLM configuration extraction from manifest."""

    def test_get_llm_config_no_router(self):
        """Test _get_llm_config returns None when no router found."""
        compiler = LangGraphCompiler()
        compiler._manifest = Mock()
        compiler._manifest.routers = []

        node = Mock()
        node.router_ref = None
        node.router = None

        llm, system_msg = compiler._get_llm_config(node)

        assert llm is None
        assert system_msg is None

    def test_get_llm_config_with_router_ref(self):
        """Test _get_llm_config extracts config from router_ref."""
        compiler = LangGraphCompiler()

        # Create mock router
        router = Mock()
        router.name = "my_router"
        router.default_model = "ollama://llama3"
        router.model_candidates = None
        router.system_message = "You are a classifier"
        router.config = {"temperature": 0.1}

        compiler._manifest = Mock()
        compiler._manifest.routers = [router]

        node = Mock()
        node.router_ref = "my_router"
        node.router = None

        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.LLMFactory.create"
        ) as mock_create:
            mock_llm = Mock()
            mock_create.return_value = mock_llm

            llm, system_msg = compiler._get_llm_config(node)

            assert llm == mock_llm
            assert system_msg == "You are a classifier"
            mock_create.assert_called_once()

    def test_get_llm_config_with_router_object(self):
        """Test _get_llm_config handles RouterRef object."""
        compiler = LangGraphCompiler()

        router = Mock()
        router.name = "my_router"
        router.default_model = "openai://gpt-4"
        router.model_candidates = None
        router.system_message = None
        router.config = {}

        compiler._manifest = Mock()
        compiler._manifest.routers = [router]

        # router is a RouterRef object with .name
        router_ref = Mock()
        router_ref.name = "my_router"

        node = Mock()
        node.router_ref = None
        node.router = router_ref

        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.LLMFactory.create"
        ) as mock_create:
            mock_llm = Mock()
            mock_create.return_value = mock_llm

            llm, system_msg = compiler._get_llm_config(node)

            assert llm == mock_llm


class TestRouterNode:
    """Test router node async function."""

    @pytest.mark.asyncio
    async def test_router_node_invokes_llm(self):
        """Test router node invokes LLM and returns response."""
        compiler = LangGraphCompiler()

        # Setup mock router
        router = Mock()
        router.name = "test_router"
        router.default_model = "openai://gpt-4"
        router.model_candidates = None
        router.system_message = "Classify the input"
        router.config = {}

        compiler._manifest = Mock()
        compiler._manifest.routers = [router]

        node = Mock()
        node.id = "router_node"
        node.router_ref = "test_router"
        node.router = None

        with patch(
            "universal_agent_nexus.adapters.langgraph.compiler.LLMFactory.create"
        ) as mock_create:
            mock_llm = AsyncMock()
            mock_response = Mock()
            mock_response.content = "safe"
            mock_llm.ainvoke.return_value = mock_response
            mock_create.return_value = mock_llm

            router_fn = compiler._create_router_node(node)

            # Execute router
            state = {"messages": [Mock(content="Hello world")]}
            result = await router_fn(state)

            # Should have called LLM
            mock_llm.ainvoke.assert_called_once()

            # Should return messages with response
            assert "messages" in result
            assert mock_response in result["messages"]

    @pytest.mark.asyncio
    async def test_router_node_handles_missing_config(self):
        """Test router node handles missing LLM config gracefully."""
        compiler = LangGraphCompiler()
        compiler._manifest = Mock()
        compiler._manifest.routers = []

        node = Mock()
        node.id = "router_no_config"
        node.router_ref = None
        node.router = None

        router_fn = compiler._create_router_node(node)

        state = {"messages": []}
        result = await router_fn(state)

        # Should return state unchanged
        assert result == state


class TestPassthroughNode:
    """Test passthrough (task) node."""

    @pytest.mark.asyncio
    async def test_passthrough_node_returns_state(self):
        """Test passthrough node returns state unchanged."""
        compiler = LangGraphCompiler()

        passthrough_fn = compiler._create_passthrough_node("my_task")

        state = {"messages": [Mock(content="test")]}
        result = await passthrough_fn(state)

        assert result == state


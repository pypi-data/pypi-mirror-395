"""
IR Visitor Pattern for analysis and transformation.

Standard way to analyze and transform IR without coupling to structure.
"""

from abc import ABC, abstractmethod

from . import EdgeIR, GraphIR, ManifestIR, NodeIR, RouterIR, ToolIR


class IRVisitor(ABC):
    """
    Visitor pattern for IR traversal.

    Standard way to analyze and transform IR without coupling to structure.
    """

    @abstractmethod
    def visit_manifest(self, ir: ManifestIR) -> None:
        """Visit ManifestIR."""
        pass

    @abstractmethod
    def visit_graph(self, graph: GraphIR) -> None:
        """Visit GraphIR."""
        pass

    @abstractmethod
    def visit_node(self, node: NodeIR) -> None:
        """Visit NodeIR."""
        pass

    @abstractmethod
    def visit_edge(self, edge: EdgeIR) -> None:
        """Visit EdgeIR."""
        pass

    @abstractmethod
    def visit_tool(self, tool: ToolIR) -> None:
        """Visit ToolIR."""
        pass

    @abstractmethod
    def visit_router(self, router: RouterIR) -> None:
        """Visit RouterIR."""
        pass


class DefaultIRVisitor(IRVisitor):
    """
    Base visitor with default no-op implementations.

    Subclass this and override only the methods you need.
    """

    def visit_manifest(self, ir: ManifestIR) -> None:
        """Visit all graphs, tools, and routers in manifest."""
        for graph in ir.graphs:
            self.visit_graph(graph)
        for tool in ir.tools:
            self.visit_tool(tool)
        for router in ir.routers:
            self.visit_router(router)

    def visit_graph(self, graph: GraphIR) -> None:
        """Visit all nodes and edges in graph."""
        for node in graph.nodes:
            self.visit_node(node)
        for edge in graph.edges:
            self.visit_edge(edge)

    def visit_node(self, node: NodeIR) -> None:
        """Visit node (no-op by default)."""
        pass

    def visit_edge(self, edge: EdgeIR) -> None:
        """Visit edge (no-op by default)."""
        pass

    def visit_tool(self, tool: ToolIR) -> None:
        """Visit tool (no-op by default)."""
        pass

    def visit_router(self, router: RouterIR) -> None:
        """Visit router (no-op by default)."""
        pass


def traverse(ir: ManifestIR, visitor: IRVisitor) -> None:
    """
    Traverse IR with visitor.

    Args:
        ir: ManifestIR to traverse
        visitor: IRVisitor instance

    Example:
        from universal_agent_nexus.ir.visitor import DefaultIRVisitor, traverse

        class CostAnalyzer(DefaultIRVisitor):
            def __init__(self):
                self.total_cost = 0.0

            def visit_node(self, node):
                cost = node.metadata.get_annotation(CostAnnotation)
                if cost:
                    self.total_cost += cost.cost_cents / 100

        analyzer = CostAnalyzer()
        traverse(ir, analyzer)
        print(f"Total estimated cost: ${analyzer.total_cost}")
    """
    visitor.visit_manifest(ir)


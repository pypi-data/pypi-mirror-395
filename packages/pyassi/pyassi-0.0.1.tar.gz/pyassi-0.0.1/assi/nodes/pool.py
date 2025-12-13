from typing import TYPE_CHECKING, Callable, Iterable, Tuple
from typing import Hashable, Any
from logging import getLogger
from networkx.classes import DiGraph
from networkx.algorithms.dag import topological_sort

from .node import Node, ExecutionContext, _Y


logger = getLogger(__name__)


class PoolFeatures(dict):
    """Only for type checking"""

    if TYPE_CHECKING:

        def __getitem__(self, key: Node[Any, _Y]) -> _Y: ...


NodeExecutionDoneCallback = Callable[[Node[Any, _Y], _Y], None]


class Pool:
    def __init__(
        self,
        nodes: Iterable[Node[Any, Any]],
        node_execution_done_callback: NodeExecutionDoneCallback | None = None,
    ):
        """Pool class. It's aim is to contain many nodes, and execute them in topological order.

        Parameters
        ----------
        nodes : Iterable[Node[Any, Any]]
            Iterable of nodes
        node_execution_done_callback : NodeExecutionDoneCallback | None, optional
            Done callback, which is called when the node is finished the execution, by default None
        """
        self.__nodes = tuple(nodes)
        self.node_execution_done_callback = node_execution_done_callback

    @property
    def nodes(self) -> Tuple[Node[Any, Any], ...]:
        """Nodes in the pool

        Returns
        -------
        Tuple[Node[Any, Any], ...]
            Tuple of nodes
        """
        return self.__nodes

    def graph(self) -> "DiGraph[Node[Any, Any]]":
        """Create a directed graph representing the dependencies between nodes in the pool.

        Returns
        -------
        DiGraph[Node[Any, Any]]
            Directed graph of nodes with edges representing dependencies
        """
        graph: DiGraph[Node[Any, Any]] = DiGraph()

        # add edges for the current pool
        def add_edges_for_pool(node: Node[Any, Any]):
            for parent in node.node_parents:
                graph.add_edge(parent, node)
                add_edges_for_pool(parent)

        for node in self.nodes:
            add_edges_for_pool(node)

        return graph

    def execute(self, x: Hashable) -> PoolFeatures:
        """Execute all nodes in the pool in topological order.

        Parameters
        ----------
        x : Hashable
            Input data for execution

        Returns
        -------
        PoolFeatures
            Results of the execution
        """
        graph = self.graph()

        results = PoolFeatures()
        # prepare context
        context = ExecutionContext(x=x, pool=self)
        try:
            logger.debug(
                f"Starting execution of {graph.number_of_nodes()} nodes in the {self}"
            )

            for node in topological_sort(graph):
                result = node.node_execute(context)
                results[node] = result
                # call the done callback if provided
                if self.node_execution_done_callback:
                    self.node_execution_done_callback(node, result)

            logger.debug(f"Finished execution in {self}")

        finally:
            # clear cache for all nodes
            for node in graph.nodes:
                node.node_clear_cache(context)

        return results

    def __str__(self) -> str:
        return f"pool at {hex(id(self))} ({type(self).__name__})"

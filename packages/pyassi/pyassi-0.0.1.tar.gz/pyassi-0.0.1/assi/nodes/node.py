from typing import Tuple, Dict, Type, Union, Set
from typing import overload
from typing import Hashable, NamedTuple
from typing import Generic, TypeVar
from typing import TYPE_CHECKING
from abc import abstractmethod
from typing import Any
from logging import getLogger


if TYPE_CHECKING:
    from .pool import Pool


logger = getLogger(__name__)


_V = TypeVar("_V", bound=Hashable)
_X = TypeVar("_X", bound=Hashable)
_Y = TypeVar("_Y", bound=Any)


class ExecutionContext(Generic[_X], NamedTuple):
    """Execution context for node evaluation.

    Encapsulates the input data and the pool context in which a node is executed.
    This allows nodes to access both the computation input and pool information.
    """

    x: _X
    pool: Union["Pool", None]

    @classmethod
    def from_x(cls: Type["ExecutionContext[_V]"], x: _V) -> "ExecutionContext[_V]":
        """Create a new ExecutionContext containing a single value.

        This convenience constructor wraps the provided value `x` in an ExecutionContext
        with the `pool` field set to None.

        Parameters
        ----------
        x : _V
            The value to store in the new execution context.

        Returns
        -------
        ExecutionContext[_V]
            A new ExecutionContext instance containing `x` with `pool=None`.
        """
        return cls(x=x, pool=None)


def cache_key(context: ExecutionContext[Any]) -> Hashable:
    """Generate a cache key from an execution context.

    Parameters
    ----------
    context : ExecutionContext[Any]
        The execution context.

    Returns
    -------
    Hashable
        A cache key derived from the context's pool and input value.
    """
    return frozenset((context.pool, context.x))


def node_in_pool_str(node: "Node", pool: Union["Pool", None]) -> str:
    """Generate a string representation of a node and its pool for logging.

    Parameters
    ----------
    node : Node
        The node to represent.
    pool : Union[Pool, None]
        The pool in which the node is executed, or None for the global pool.

    Returns
    -------
    str
        A formatted string describing the node and its execution pool.
    """
    pool_name = pool if pool else "global pool"

    return f"the {node} in the {pool_name}"


class Node(Generic[_X, _Y]):
    """A node in a computation graph.

    Nodes represent computation units that transform input data of type `_X` into output
    data of type `_Y`. Nodes support result caching and parent-child relationships within
    a computation graph.
    """

    _nodes: Dict[str, "Node[Any, Any]"] = {}

    if TYPE_CHECKING:
        _node_name: str
        _node_parents: Set["Node[_X, _Y]"]
        _node_cache: Dict[Hashable, _Y]

    @classmethod
    def register_node(cls, name: str, node: "Node[Any, Any]"):
        """Register a node with a unique name.

        Each registered node name must be unique within the process. A node can only
        be registered once.

        Parameters
        ----------
        name : str
            The node name. Must be unique for the process and non-empty.
        node : Node[Any, Any]
            The node instance to register.

        Raises
        ------
        ValueError
            If the name is an empty string.
        ValueError
            If a node with the same name has already been registered.
        ValueError
            If the node instance is already registered under a different name.
        """
        if name == "":
            raise ValueError("Node name cannot be empty.")
        if name in cls._nodes:
            raise ValueError("Node with the same has been registered.")
        if node in cls._nodes.values():
            raise ValueError("The node is already registered.")

        cls._nodes[name] = node
        logger.debug(f"Registered {node}")

    @classmethod
    def node_get(cls, name: str) -> Union["Node[Any, Any]", None]:
        """Retrieve a registered node by name.

        Parameters
        ----------
        name : str
            The unique name of the node to retrieve.

        Returns
        -------
        Node | None
            The node instance if registered with the given name, otherwise None.
        """
        if name not in cls._nodes:
            return None
        return cls._nodes[name]

    @property
    def node_name(self) -> str | None:
        """The registered name of this node.

        Returns
        -------
        str | None
            The node's registered name, or None if the node has not been registered.
        """
        if hasattr(self, "_node_name"):
            return self._node_name

        for name, node in self.__class__._nodes.items():
            if node is self:
                self._node_name = name
                return name
        return None

    @property
    def node_parents(self) -> Tuple["Node[Any, Any]", ...]:
        """Parent nodes in the computation graph.

        Returns
        -------
        Tuple[Node[Any, Any], ...]
            A tuple of parent nodes, or an empty tuple if this node has no parents.
        """
        parents = getattr(self, "_node_parents", None)
        if parents is None:
            return tuple()
        else:
            return tuple(parents)

    def __setattr__(self, name: str, value: Any) -> None:
        # This function adds parent nodes when setting attributes,
        # allowing users to simply write `self.parent_node = ...`.
        if isinstance(value, Node):
            parents = getattr(self, "_node_parents", None)
            if parents is None:
                self._node_parents = {value}
            else:
                self._node_parents.add(value)
        return super().__setattr__(name, value)

    @staticmethod
    def _node_prepare_context(
        context: ExecutionContext[_X] | _X,
    ) -> ExecutionContext[_X]:
        """Convert input to an ExecutionContext.

        If the input is not already an ExecutionContext, it is wrapped in one with
        `pool=None`.

        Parameters
        ----------
        context : ExecutionContext[_X] | _X
            An execution context or raw input data.

        Returns
        -------
        ExecutionContext[_X]
            An execution context ready for node execution.
        """
        if not isinstance(context, ExecutionContext):
            context = ExecutionContext.from_x(context)
            return context
        else:
            return context

    @abstractmethod
    def __execute__(self, context: ExecutionContext[_X]) -> _Y: ...

    @overload
    def node_execute(self, context: _X) -> _Y: ...

    @overload
    def node_execute(self, context: ExecutionContext[_X]) -> _Y: ...

    def node_execute(self, context: ExecutionContext[_X] | _X) -> _Y:
        """Execute the node and cache the result.

        This method wraps the core `__execute__` computation with context preparation
        and result caching.

        Parameters
        ----------
        context : ExecutionContext[_X] | _X
            An execution context or raw input data.

        Returns
        -------
        _Y
            The execution result, retrieved from cache if available.
        """
        # prepare context
        context = self._node_prepare_context(context)

        # create cache if it does not exist
        if not hasattr(self, "_node_cache"):
            self._node_cache = {}

        # get result from cache if any
        key = cache_key(context)
        if key in self._node_cache:
            return self._node_cache[key]

        logger.debug(f"Starting execution of {node_in_pool_str(self, context.pool)}")

        result = self.__execute__(context)
        self._node_cache[key] = result

        logger.debug(f"Finished execution of {node_in_pool_str(self, context.pool)}")

        return result

    def node_clear_cache(
        self,
        context: ExecutionContext[_X] | _X,
        recursive: bool = False,
    ) -> None:
        """Clear cached results for the given execution context.

        Parameters
        ----------
        context : ExecutionContext[_X] | _X
            An execution context or raw input data.
        recursive : bool, optional
            If True, recursively clear caches of parent nodes. Default is False.
        """
        # prepare context
        context = self._node_prepare_context(context)

        key = cache_key(context)

        # remove result from cache if any
        if hasattr(self, "_node_cache"):
            self._node_cache.pop(key, None)

        logger.debug(f"Cleared cache of {node_in_pool_str(self, context.pool)}")

        # remove recursively
        if recursive:
            for parent in self.node_parents:
                parent.node_clear_cache(context, recursive)

    def __str__(self) -> str:
        node_name = self.node_name
        if node_name:
            return f'node "{node_name}" ({type(self).__name__})'

        return f"node at {hex(id(self))} ({type(self).__name__})"

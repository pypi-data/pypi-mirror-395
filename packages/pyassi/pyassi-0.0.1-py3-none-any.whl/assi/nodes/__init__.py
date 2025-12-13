"""The `assi.nodes` module provides the core computation graph framework with node registration, execution context management, and caching capabilities.
Nodes represent computation units in a directed acyclic graph (DAG) executed in pools.
"""

from .node import Node, ExecutionContext
from .pool import Pool

from .pydantic import HashableBaseModel, SerializedTorchTensor


__all__ = (
    "Node",
    "ExecutionContext",
    "Pool",
    "HashableBaseModel",
    "SerializedTorchTensor",
)

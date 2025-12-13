from .node import Node
from ..modelstorage import ModelStorage


from jsonargparse._util import import_object
from typing import TypeVar, Type
import lightning as L


_LightningModuleType = TypeVar("_LightningModuleType", bound=L.LightningModule)


def lightning_node_factory(
    name: str,
    model_type: str | Type[_LightningModuleType],
    model_storage: ModelStorage,
    model_kwargs: dict | None = None,
) -> _LightningModuleType:
    """
    Factory function to create or retrieve a LightningModule-based Node instance.

    This function handles the creation of nodes that are based on PyTorch Lightning modules.
    It first checks if a node with the given name already exists in the registry. If it does,
    the existing node is returned. Otherwise, a new node is created by either loading from
    a checkpoint (if available) or instantiating a new module with the provided keyword
    arguments.

    Parameters
    ----------
    name : str
        The name to register the node under or retrieve from the registry.
    model_type : str or Type[_LightningModuleType]
        Either a string path to a `LightningModule` class (e.g., 'module.Class')
        or the class type itself. The class must be a subclass of both `LightningModule`
        and `Node`.
    model_storage : ModelStorage
        A ModelStorage instance that manages the checkpoint path for
        loading pre-trained models.
    model_kwargs : dict or None, optional
        Optional dictionary of keyword arguments to pass to the module
        constructor when creating a new instance (used when no checkpoint is available).

    Returns
    -------
    _LightningModuleType
        An instance of the specified `LightningModule` type that is also a `Node`, either
        retrieved from the registry or newly created.

    Raises
    ------
    TypeError
        If model_type is not a subclass of `LightningModule` or `Node`, or if a
        node with the given name exists but is not an instance of the requested class.

    Examples
    --------
    >>> storage = ModelStorage(checkpoint_path="path/to/model.ckpt")
    >>> node = lightning_node_factory("my_model", "models.MyModel", storage)
    """
    # If string, import a class
    if isinstance(model_type, str):
        cls: Type[_LightningModuleType] = import_object(model_type)
    else:
        cls = model_type

    # Ensure the imported object is a LightningModule subclass
    if not issubclass(cls, L.LightningModule):
        raise TypeError(f"{model_type} is not a subclass of LightningModule")
    # Ensure it is also a Node subclass
    if not issubclass(cls, Node):
        raise TypeError(f"{model_type} is not a subclass of Node")

    # If node already exists in registry
    if node := Node.node_get(name):
        if not isinstance(node, cls):  # type: ignore
            raise TypeError(f"Node registered under {name} is not an instance of {cls}")
        return node  # pyrefly: ignore[bad-return]

    # Load a new model-node from checkpoint
    model_storage.check_integrity()
    checkpoint_path = model_storage.checkpoint_path

    if checkpoint_path is not None:
        module = cls.load_from_checkpoint(checkpoint_path)
    else:
        module = cls(**(model_kwargs or {}))  # pyrefly: ignore[not-callable]

    module.eval()
    module.freeze()

    # Register the node
    Node.register_node(name, module)

    return module

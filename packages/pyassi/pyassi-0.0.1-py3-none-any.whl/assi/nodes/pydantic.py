import torch
from typing import Hashable, List, Literal
from typing import TYPE_CHECKING
from pydantic import GetCoreSchemaHandler, ValidatorFunctionWrapHandler
from pydantic import BaseModel, ConfigDict
from pydantic_core import core_schema
import base64


class HashableBaseModel(BaseModel, Hashable):
    """Immutable, hashable Pydantic model used as node input or cache key.

    Instances of this model are frozen via `ConfigDict(frozen=True)`, making them
    safe to use as dictionary keys or cache keys.
    """

    model_config = ConfigDict(frozen=True)

    if TYPE_CHECKING:

        def __hash__(self) -> int: ...


class _SerializedTorchTensorData(BaseModel):
    type: Literal["torch"]
    dtype: str
    shape: List[int]
    stride: List[int]
    storage_offset: int
    bytes: str


class SerializedTorchTensor:
    """Helper for serializing and deserializing torch.Tensor objects.

    Notes
    -------
    You can annotate torch.Tensor fields in Pydantic models using this class:
    ```
    class A(HashableBaseModel):
        tensor: Annotated[torch.Tensor, SerializedTorchTensor]
    ```

    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler: GetCoreSchemaHandler):
        # Return a pydantic-core schema wrapper that validates torch.Tensor instances
        # and provides a custom serializer for storing tensor metadata.
        return core_schema.no_info_wrap_validator_function(
            function=cls.validate,
            schema=core_schema.is_instance_schema(torch.Tensor),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize,
                return_schema=handler.generate_schema(_SerializedTorchTensorData),
            ),
        )

    @staticmethod
    def validate(value, handler: ValidatorFunctionWrapHandler):
        """Validate or coerce a value into a `torch.Tensor`.

        Accepts either a ``torch.Tensor`` instance or a mapping matching
        ``_SerializedTorchTensorData`` and returns a reconstructed ``torch.Tensor``.
        """
        if isinstance(value, torch.Tensor):
            return value

        tensor_data = _SerializedTorchTensorData(**value)

        data = base64.b64decode(tensor_data.bytes)
        tensor = torch.frombuffer(
            bytearray(data),
            dtype=getattr(torch, tensor_data.dtype),
        )
        return tensor.as_strided(
            size=tensor_data.shape,
            stride=tensor_data.stride,
            storage_offset=tensor_data.storage_offset,
        )

    @staticmethod
    def serialize(tensor: torch.Tensor) -> _SerializedTorchTensorData:
        """Serialize a ``torch.Tensor`` into a Pydantic-friendly data model.

        The returned ``_SerializedTorchTensorData`` contains metadata required to
        reconstruct the tensor (dtype, shape, stride, storage offset) and a
        base64-encoded byte payload of the tensor buffer.
        """
        arr = tensor.cpu().numpy()
        return _SerializedTorchTensorData(
            type="torch",
            dtype=str(tensor.dtype).replace("torch.", ""),
            shape=list(tensor.shape),
            stride=list(tensor.stride()),
            storage_offset=int(tensor.storage_offset()),
            bytes=base64.b64encode(arr.tobytes()).decode(),
        )

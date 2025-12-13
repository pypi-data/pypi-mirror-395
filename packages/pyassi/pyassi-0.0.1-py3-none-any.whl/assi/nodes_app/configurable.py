from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict


class ConfigurableConfig(BaseModel):
    model_config = ConfigDict(frozen=True)


_ConfigurableConfig = TypeVar("_ConfigurableConfig", bound=ConfigurableConfig)


class Configurable(Generic[_ConfigurableConfig]):
    def __init__(self, config: _ConfigurableConfig) -> None:
        self.__config = config

    @property
    def config(self) -> _ConfigurableConfig:
        return self.__config

    @config.setter
    def config(self, value: _ConfigurableConfig) -> None:
        self.__config = value

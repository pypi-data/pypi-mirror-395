from typing import Annotated, Type
from fastapi import APIRouter, Depends
from assi.nodes import Node
from .pool_service import PoolService, PoolServiceProxy
from .configurable import ConfigurableConfig


def create_pool_type_router(
    pool_type: Type[PoolService],
    pool_services: dict[str, PoolServiceProxy],
) -> APIRouter:
    router = APIRouter(prefix=f"/{pool_type.__name__}")

    def pool_service(pool_id: str) -> PoolServiceProxy:
        return pool_services[pool_id]

    async def start(
        pool_service: Annotated[PoolServiceProxy, Depends(pool_service)],
    ):
        await pool_service.start()

    async def stop(
        pool_service: Annotated[PoolServiceProxy, Depends(pool_service)],
    ):
        await pool_service.stop()

    router.add_api_route("/stop", stop, methods=["POST"])
    router.add_api_route("/start", start, methods=["POST"])

    return router


def create_node_type_router(
    node_type: Type[Node],
    pool_services: dict[str, PoolServiceProxy],
    node_config_type: Type[ConfigurableConfig] | None = None,
) -> APIRouter:
    router = APIRouter(prefix=f"/{node_type.__name__}")

    def pool_service(pool_id: str) -> PoolServiceProxy:
        return pool_services[pool_id]

    if node_config_type is None:
        return router

    async def get_config(
        node_name: str,
        pool_service: Annotated[PoolServiceProxy, Depends(pool_service)],
    ) -> Annotated[ConfigurableConfig, node_config_type]:
        raw_config = await pool_service.get_config(node_name)

        assert node_config_type is not None

        return node_config_type.model_validate_json(raw_config)

    async def set_config(
        node_name: str,
        config: Annotated[ConfigurableConfig, node_config_type],
        pool_service: Annotated[PoolServiceProxy, Depends(pool_service)],
    ):
        await pool_service.set_config(node_name, config.model_dump_json())

    router.add_api_route("/config", get_config, methods=["GET"])
    router.add_api_route("/config", set_config, methods=["POST"])

    return router

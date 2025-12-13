from abc import abstractmethod
from typing import Any, Generic, TypeVar
import logging
import threading
import asyncio
from enum import StrEnum

import zmq
import zmq.asyncio
from pydantic import BaseModel

from assi.nodes import Node, Pool
from assi.nodes_app.configurable import Configurable, ConfigurableConfig

logger = logging.getLogger(__name__)


# Command constants
class Commands(StrEnum):
    START = "start"
    STOP = "stop"
    GET_CONFIG = "get_config"
    SET_CONFIG = "set_config"


class NodeResults(BaseModel):
    pool_id: str
    node_name: str
    node_type: str
    result: Any


_X = TypeVar("_X", bound=Any)


class PoolService(Generic[_X]):
    def __init__(
        self,
        pool_id: str,
        addr: str,
        broker_addr: str,
        nodes: dict[str, Node[_X, Any]],
    ) -> None:
        """Service for managing a pool of nodes over ZMQ sockets.
        Provides command handling for node execution control and configuration management.


        Parameters
        ----------
        pool_id : str
            Unique identifier for this pool
        addr : str
            ZMQ address to bind to (e.g., 'tcp://127.0.0.1:5555')
        broker_addr : str
            ZMQ address of the broker to connect to
        nodes : dict[str, Node[_X, Any]]
            Dictionary mapping node names to Node instances
        """
        self.pool_id = pool_id
        self.nodes = nodes
        self.should_stop = True
        self.lock = threading.Lock()
        self.thread: None | threading.Thread = None

        # Initialize ZMQ context and sockets
        self.ctx = zmq.sugar.Context()

        self.socket = self.ctx.socket(zmq.REP)
        self.socket.bind(addr)
        logger.info(f"PoolService {pool_id} bound to {addr}")

        self.broker_socket = self.ctx.socket(zmq.PUSH)
        self.broker_socket.connect(broker_addr)
        self.broker_socket.setsockopt(zmq.SNDHWM, 1)  # Limit queue size
        self.broker_socket.setsockopt(zmq.SNDTIMEO, 1000)  # 1 second timeout
        logger.info(f"PoolService {pool_id} connected to broker at {broker_addr}")

        # Register and initialize pool
        for node_name, node in nodes.items():
            Node.register_node(node_name, node)

        self.pool = Pool(
            nodes=nodes.values(),
            node_execution_done_callback=self.node_execution_done_callback,
        )

    def node_execution_done_callback(self, node: Node, result: Any) -> None:
        """Callback invoked when a node completes execution.

        Parameters
        ----------
        node : Node
            The node that completed
        result : Any
            The result from the node execution
        """
        node_name = node.node_name or str(type(node).__name__)

        try:
            self.broker_socket.send_string(
                NodeResults(
                    pool_id=self.pool_id,
                    node_name=node_name,
                    node_type=type(node).__name__,
                    result=result,
                ).model_dump_json()
            )
        except zmq.error.Again:
            logger.warning(f"Broker timeout sending result from node {node_name}")
        except Exception as e:
            logger.error(f"Error sending node result: {e}", exc_info=True)

    def _get_configurable_node(self, node_name: str) -> Configurable | None:
        """Get a configurable node by name.

        Parameters
        ----------
        node_name: str
            Name of the node

        Returns
        -------
        Configurable | None
            The node if it exists and is Configurable, None otherwise
        """
        if node_name not in self.nodes:
            logger.warning(f"Node {node_name} not found")
            return None

        node = self.nodes[node_name]
        if not isinstance(node, Configurable):
            logger.warning(f"Node {node_name} is not Configurable")
            return None

        return node

    def _handle_get_config(self, node_name: str) -> tuple[bool, str | None]:
        """Handle get_config command.

        Parameters
        ----------
        node_name: str
            Name of the node

        Returns
        -------
        tuple[bool, str | None]
            Tuple of (success, config_json)
        """
        node = self._get_configurable_node(node_name)
        if node is None:
            return False, None

        try:
            config: ConfigurableConfig = node.config
            return True, config.model_dump_json()
        except Exception as e:
            logger.error(f"Error retrieving config for {node_name}: {e}", exc_info=True)
            return False, None

    def _handle_set_config(self, node_name: str, payload: str) -> bool:
        """Handle set_config command.

        Parameters
        ----------
        node_name: str
            Name of the node
        payload: str
            JSON string with new config

        Returns
        -------
        bool
            True if successful, False otherwise
        """
        node = self._get_configurable_node(node_name)
        if node is None:
            return False

        try:
            config: ConfigurableConfig = node.config
            with self.lock:
                node.config = config.__class__.model_validate_json(payload)
            logger.info(f"Config updated for node {node_name}")
            return True
        except ValueError as e:
            logger.error(f"Invalid config JSON for {node_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error setting config for {node_name}: {e}", exc_info=True)
            return False

    def _handle_start(self) -> bool:
        """Handle start command.

        Returns
        -------
        bool
            True if started successfully
        """
        with self.lock:
            if self.thread is None or not self.thread.is_alive():
                self.should_stop = False
                self.thread = threading.Thread(target=self.start, daemon=True)
                self.thread.start()
                logger.info(f"Pool {self.pool_id} started")
                return True
        logger.warning(f"Pool {self.pool_id} already running")
        return True

    def _handle_stop(self) -> bool:
        """Handle stop command.

        Returns
        -------
        bool
            True if stopped successfully
        """
        with self.lock:
            self.should_stop = True

        if self.thread is not None and self.thread.is_alive():
            self.thread.join(timeout=5)

        self.thread = None
        logger.info(f"Pool {self.pool_id} stopped")
        return True

    def start_service(self) -> None:
        """Start the service and listen for commands.

        Blocks indefinitely, listening for commands on the ZMQ socket.
        Commands handled: start, stop, get_config, set_config
        """
        logger.info(f"PoolService {self.pool_id} starting command loop")

        while True:
            try:
                raw_data = self.socket.recv_multipart()
                cmd, node_name, payload = map(lambda x: x.decode("utf-8"), raw_data)

                success = False
                response = ""

                if cmd == Commands.START:
                    success = self._handle_start()
                    response = cmd if success else ""

                elif cmd == Commands.STOP:
                    success = self._handle_stop()
                    response = cmd if success else ""

                elif cmd == Commands.GET_CONFIG:
                    success, config_json = self._handle_get_config(node_name)
                    if success and config_json:
                        self.socket.send_multipart(
                            (cmd.encode("utf-8"), config_json.encode("utf-8"))
                        )
                        continue
                    response = ""

                elif cmd == Commands.SET_CONFIG:
                    success = self._handle_set_config(node_name, payload)
                    response = cmd if success else ""

                else:
                    logger.warning(f"Unknown command: {cmd}")
                    response = ""

                self.socket.send_string(response)

            except zmq.error.ContextTerminated:
                logger.info("Socket context terminated, exiting service loop")
                break
            except Exception as e:
                logger.error(f"Error in service loop: {e}", exc_info=True)
                try:
                    self.socket.send_string("")
                except Exception as send_error:
                    logger.error(f"Error sending error response: {send_error}")

    @abstractmethod
    def start(self) -> None:
        """Start the pool execution loop.

        This method should be implemented by subclasses to define
        how the pool should execute nodes.

        Should check `self.should_stop` in a loop and return when it becomes `True`:
        ```
        while True:
            with self.lock:
                if self.should_stop:
                    return

            with self.lock:
                ... # Perform calculations

            ... # Send results
        ```

        """
        while True:
            with self.lock:
                if self.should_stop:
                    return
            ...

    def __del__(self) -> None:
        """Clean up resources."""
        try:
            self.should_stop = True
            if self.thread is not None and self.thread.is_alive():
                self.thread.join(timeout=5)
            self.socket.close()
            self.broker_socket.close()
            self.ctx.term()
            logger.info(f"PoolService {self.pool_id} cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)


class PoolServiceProxy:
    """Async proxy client for communicating with a PoolService.

    Provides an async interface to send commands to a PoolService instance.
    """

    def __init__(self, addr: str) -> None:
        """Initialize the proxy.

        Parameters
        ----------
        addr: str
            ZMQ address of the PoolService (e.g., 'tcp://127.0.0.1:5555')
        """
        self.addr = addr
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, 10000)  # 10 second timeout
        self.socket.connect(addr)
        logger.info(f"PoolServiceProxy connected to {addr}")

        self.recv_lock = asyncio.Lock()

    async def _recv(
        self,
        cmd: str,
        node_name: str | None = None,
        payload: str | None = None,
    ) -> str | None:
        """Send a command and receive a response.

        Parameters
        ----------
        cmd: str
            Command to send
        node_name: str | None
            Optional node name
        payload: str | None
            Optional payload data

        Returns
        -------
        str | None
            Response payload, or None if single-part response

        Raises
        ------
        ValueError
            If response format is invalid or doesn't match command
        zmq.error.Again
            If timeout occurs
        """
        async with self.recv_lock:
            try:
                await self.socket.send_multipart(
                    (
                        cmd.encode("utf8"),
                        (node_name if node_name is not None else "").encode("utf8"),
                        (payload if payload is not None else "").encode("utf8"),
                    )
                )
                raw_response = await self.socket.recv_multipart()
            except zmq.error.Again:
                logger.error(f"Timeout waiting for response to command: {cmd}")
                raise

        # Parse response
        if len(raw_response) == 2:
            resp_cmd, resp_payload = raw_response
            response = resp_payload.decode("utf8")
        elif len(raw_response) == 1:
            resp_cmd = raw_response[0]
            response = None
        else:
            raise ValueError(f"Unexpected response length: {len(raw_response)}")

        resp_cmd_str = resp_cmd.decode("utf8")
        if resp_cmd_str != cmd:
            raise ValueError(
                f"Response command mismatch: expected '{cmd}', got '{resp_cmd_str}'"
            )

        return response

    async def set_config(self, node_name: str, config: str) -> None:
        """Set configuration for a node.

        Parameters
        ----------
        node_name: str
            Name of the node
        config: str
            JSON string with configuration

        Raises
        ------
        ValueError
            If node not found or config invalid
        zmq.error.Again
            If timeout occurs
        """
        response = await self._recv(
            Commands.SET_CONFIG, node_name=node_name, payload=config
        )
        if not response:
            raise ValueError(f"Failed to set config for node {node_name}")
        logger.info(f"Config set for node {node_name}")

    async def get_config(self, node_name: str) -> str:
        """Get configuration for a node.

        Parameters
        ----------
        node_name: str
            Name of the node

        Returns
        -------
        str
            JSON string with configuration

        Raises
        ------
        ValueError
            If node not found
        zmq.error.Again
            If timeout occurs
        """
        response = await self._recv(Commands.GET_CONFIG, node_name=node_name)
        if response is None:
            raise ValueError(f"Failed to get config for node {node_name}")
        return response

    async def start(self) -> None:
        """Start the pool execution."""
        await self._recv(Commands.START)
        logger.info(f"Sent start command to {self.addr}")

    async def stop(self) -> None:
        """Stop the pool execution."""
        await self._recv(Commands.STOP)
        logger.info(f"Sent stop command to {self.addr}")

    async def __del__(self) -> None:
        """Close the connection."""
        try:
            self.socket.close()
            self.ctx.term()
            logger.info(f"PoolServiceProxy connection to {self.addr} closed")
        except Exception as e:
            logger.error(f"Error closing proxy connection: {e}", exc_info=True)

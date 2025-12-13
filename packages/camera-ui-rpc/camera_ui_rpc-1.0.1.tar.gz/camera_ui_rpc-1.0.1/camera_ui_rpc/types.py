"""Type definitions for camera.ui RPC library."""

from __future__ import annotations

import ssl
from collections.abc import Callable, Coroutine
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    NotRequired,
    Protocol,
    TypedDict,
    TypeVar,
    overload,
    runtime_checkable,
)

from nats.aio.client import Callback, Credentials, ErrorCallback, JWTCallback, SignatureCallback
from nats.aio.client import Client as NATSClient
from typing_extensions import ParamSpec

if TYPE_CHECKING:
    from .channel import Channel, PrivateChannel
    from .service import RPCService

# Type variables
T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


# Create a covariant type variable for ProxyWithClose
T_co_proxy = TypeVar("T_co_proxy", covariant=True)

CloseHandler = Callable[[], Coroutine[Any, Any, None]]


@runtime_checkable
class ProxyWithClose(Protocol[T_co_proxy]):
    @property
    def proxy(self) -> T_co_proxy: ...
    async def close(self) -> None: ...


@runtime_checkable
class RPCClient(Protocol):
    service: RPCService

    @property
    def is_connected(self) -> bool: ...
    @property
    def is_closed(self) -> bool: ...
    @property
    def max_payload_size(self) -> int: ...
    async def connect(self) -> NATSClient: ...
    async def disconnect(self) -> None: ...
    async def publish(self, subject: str, data: Any) -> None: ...
    async def subscribe(
        self,
        pattern: str,
        handler: Callable[[Any], None] | Callable[[Any], Coroutine[Any, Any, None]],
    ) -> Callable[[], Coroutine[Any, Any, None]]: ...
    async def request(self, subject: str, data: Any, timeout: int | None = None) -> Any: ...
    async def on_request(
        self, pattern: str, handler: Callable[[Any], Any | Coroutine[Any, Any, Any]]
    ) -> Callable[[], Coroutine[Any, None, None]]: ...
    async def register_handler(
        self, namespace: str, handlers: object, isolated_connection: bool = False
    ) -> Callable[[], Coroutine[Any, Any, None]]: ...
    async def channel(self, channel_id: str, isolated_connection: bool = False) -> Channel: ...
    async def private_channel(
        self, channel_id: str, target_client_id: str, isolated_connection: bool = False
    ) -> PrivateChannel: ...
    @overload
    def create_proxy(
        self, namespace: str, type_class: type[T], isolated_connection: Literal[False] | None = None
    ) -> T: ...
    @overload
    def create_proxy(
        self, namespace: str, type_class: type[T], isolated_connection: Literal[True]
    ) -> ProxyWithClose[T]: ...
    @overload
    def create_proxy(
        self, namespace: str, type_class: None = None, isolated_connection: Literal[False] | None = None
    ) -> Any: ...
    @overload
    def create_proxy(
        self, namespace: str, type_class: None = None, isolated_connection: Literal[True] = True
    ) -> ProxyWithClose[Any]: ...
    def create_proxy(
        self, namespace: str, type_class: type[T] | None = None, isolated_connection: bool | None = False
    ) -> T | Any | ProxyWithClose[T] | ProxyWithClose[Any]: ...
    @overload
    async def create_service_proxy(
        self,
        service_name: str,
        type_class: type[T],
        isolated_connection: Literal[False] | None = None,
        preferred_id: str | None = None,
        timeout: int | None = None,
    ) -> T: ...
    @overload
    async def create_service_proxy(
        self,
        service_name: str,
        type_class: type[T],
        isolated_connection: Literal[True],
        preferred_id: str | None = None,
        timeout: int | None = None,
    ) -> ProxyWithClose[T]: ...
    @overload
    async def create_service_proxy(
        self,
        service_name: str,
        type_class: None = None,
        isolated_connection: Literal[False] | None = None,
        preferred_id: str | None = None,
        timeout: int | None = None,
    ) -> Any: ...
    @overload
    async def create_service_proxy(
        self,
        service_name: str,
        type_class: None = None,
        isolated_connection: Literal[True] = True,
        preferred_id: str | None = None,
        timeout: int | None = None,
    ) -> ProxyWithClose[Any]: ...
    async def create_service_proxy(
        self,
        service_name: str,
        type_class: type[T] | None = None,
        isolated_connection: bool | None = None,
        preferred_id: str | None = None,
        timeout: int | None = None,
    ) -> T | Any | ProxyWithClose[T] | ProxyWithClose[Any]: ...


class RPCAuthOptions(TypedDict):
    """Authentication options for RPC client."""

    user: str
    """Username for authentication"""

    password: str
    """Password for authentication"""


class RPCClientOptions(TypedDict):
    """Configuration options for RPC client."""

    servers: list[str]
    """NATS server URLs"""

    name: str
    """Client name for identification"""

    auth: NotRequired[RPCAuthOptions]
    """Authentication credentials with 'user' and 'pass' keys"""

    timeout: NotRequired[int]
    """Default RPC call timeout in milliseconds"""

    reconnect: NotRequired[bool]
    """Enable automatic reconnection"""

    max_reconnect_attempts: NotRequired[int]
    """Maximum reconnection attempts (-1 for infinite)"""

    reconnect_time_wait: NotRequired[int]
    """Delay between reconnection attempts in milliseconds"""

    tls: NotRequired[dict[str, str]]
    """TLS configuration with 'cert', 'key', and 'ca' keys"""

    max_payload_size: NotRequired[int]
    """Maximum payload size in bytes (default: auto-detect from NATS server)"""


class RPCMessage(TypedDict):
    """RPC request message format."""

    id: str
    """Unique request ID"""

    method: str
    """Method name to call"""

    params: Any
    """Method parameters"""

    error: NotRequired[RPCError | None]
    """Optional error (unused in requests)"""


class RPCResponse(TypedDict):
    """RPC response message format."""

    id: str
    """Request ID this response belongs to"""

    result: NotRequired[Any | None]
    """Result data (if successful)"""

    error: NotRequired[RPCError | None]
    """Error information (if failed)"""


class RPCError(TypedDict):
    """RPC error format."""

    code: str
    """Error code (see ErrorCode)"""

    message: str
    """Human-readable error message"""

    data: NotRequired[Any | None]
    """Additional error data"""


class StreamMessage(TypedDict):
    """Message format for streaming data."""

    id: str
    """Stream ID (same as request ID)"""

    type: Literal["data", "end", "error"]
    """Message type"""

    data: NotRequired[Any | None]
    """Data payload (for 'data' type)"""

    error: NotRequired[RPCError | None]
    """Error information (for 'error' type)"""


class PullIteratorRequest(TypedDict):
    """Request message for pull-based iterators."""

    id: str
    """Iterator ID"""

    type: Literal["next", "cancel"]
    """Request type"""


class PullIteratorResponse(TypedDict):
    """Response message for pull-based iterators."""

    id: str
    """Iterator ID"""

    type: Literal["value", "done", "error"]
    """Response type"""

    value: NotRequired[Any | None]
    """Value (for 'value' type)"""

    error: NotRequired[RPCError | None]
    """Error information (for 'error' type)"""


class ErrorCode(str, Enum):
    """Standard error codes."""

    METHOD_NOT_FOUND = "METHOD_NOT_FOUND"
    INVALID_PARAMS = "INVALID_PARAMS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    TIMEOUT = "TIMEOUT"
    CONNECTION_CLOSED = "CONNECTION_CLOSED"
    STREAM_ERROR = "STREAM_ERROR"
    PAYLOAD_TOO_LARGE = "PAYLOAD_TOO_LARGE"
    NOT_FOUND = "NOT_FOUND"


class ChunkedTransferHeader(TypedDict):
    """Chunked transfer header."""

    type: Literal["chunked"]
    transferId: str
    totalChunks: int
    totalSize: int


class ChunkData(TypedDict):
    """Individual chunk message."""

    transferId: str
    index: int
    data: bytes


class ConnectionOptions(TypedDict):
    servers: str | list[str]
    error_cb: NotRequired[ErrorCallback]
    disconnected_cb: NotRequired[Callback]
    closed_cb: NotRequired[Callback]
    discovered_server_cb: NotRequired[Callback]
    reconnected_cb: NotRequired[Callback]
    name: NotRequired[str]
    pedantic: NotRequired[bool]
    verbose: NotRequired[bool]
    allow_reconnect: NotRequired[bool]
    connect_timeout: NotRequired[int]
    reconnect_time_wait: NotRequired[int]
    max_reconnect_attempts: NotRequired[int]
    ping_interval: NotRequired[int]
    max_outstanding_pings: NotRequired[int]
    dont_randomize: NotRequired[bool]
    flusher_queue_size: NotRequired[int]
    no_echo: NotRequired[bool]
    tls: NotRequired[ssl.SSLContext]
    tls_hostname: NotRequired[str]
    tls_handshake_first: NotRequired[bool]
    user: NotRequired[str | None]
    password: NotRequired[str | None]
    token: NotRequired[str]
    drain_timeout: NotRequired[int]
    signature_cb: NotRequired[SignatureCallback]
    user_jwt_cb: NotRequired[JWTCallback]
    user_credentials: NotRequired[Credentials]
    nkeys_seed: NotRequired[str]
    nkeys_seed_str: NotRequired[str]
    inbox_prefix: NotRequired[str | bytes]
    pending_size: NotRequired[int]
    flush_timeout: NotRequired[float]

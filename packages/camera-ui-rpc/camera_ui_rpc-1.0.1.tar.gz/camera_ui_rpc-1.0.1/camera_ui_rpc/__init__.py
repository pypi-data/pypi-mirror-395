"""Camera UI RPC library for Python."""

# NATS service types
from nats.micro.service import ServiceConfig, ServiceInfo, ServiceStats

# Channel/PrivateChannel for bidirectional communication
from .channel import Channel, PrivateChannel

# Main client
from .client import create_rpc_client

# Decorators
from .decorators import RPCClass, RPCMethod, RPCNested, RPCProperty

# Error handling
from .errors import RPCException

# Service support
from .service import RPCService, Service

# Core types that users need
from .types import (
    CloseHandler,
    ErrorCode,
    ProxyWithClose,  # For isolated connections
    RPCClient,
    RPCClientOptions,
    RPCError,
)

__all__ = [
    # Main client
    "create_rpc_client",
    # Channels
    "Channel",
    "PrivateChannel",
    # Errors
    "RPCException",
    "ErrorCode",
    # Service
    "RPCService",
    "Service",
    # Decorators
    "RPCClass",
    "RPCMethod",
    "RPCNested",
    "RPCProperty",
    # Types
    "RPCClient",
    "RPCClientOptions",
    "RPCError",
    "ProxyWithClose",
    "CloseHandler",
    # NATS service types
    "ServiceConfig",
    "ServiceInfo",
    "ServiceStats",
]

__version__ = "1.0.0"

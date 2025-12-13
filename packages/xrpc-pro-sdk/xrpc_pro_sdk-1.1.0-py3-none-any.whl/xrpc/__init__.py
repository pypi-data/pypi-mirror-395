"""
xRPC Python SDK

Official Python SDK for xRPC - Multi-chain RPC Gateway.
"""

from .client import XRpcClient
from .methods import XRpcClientExtended
from .types import (
    XRpcError,
    Network,
    RpcType,
    JsonRpcRequest,
    JsonRpcResponse,
    XRpcConfig,
    RequestOptions,
    BatchRequestItem,
    BatchResponseItem,
    RequestMetadata,
    NetworkInfo,
    ChainInfo,
)

# WebSocket client (optional, requires websockets package)
try:
    from .websocket import (
        XRpcWebSocketClient,
        SubscriptionOptions,
        Subscription,
        SubscriptionType,
    )
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    XRpcWebSocketClient = None
    SubscriptionOptions = None
    Subscription = None
    SubscriptionType = None

__version__ = "1.1.0"
__all__ = [
    "XRpcClient",
    "XRpcClientExtended",
    "XRpcError",
    "Network",
    "RpcType",
    "JsonRpcRequest",
    "JsonRpcResponse",
    "XRpcConfig",
    "RequestOptions",
    "BatchRequestItem",
    "BatchResponseItem",
    "RequestMetadata",
    "NetworkInfo",
    "ChainInfo",
]

if WEBSOCKET_AVAILABLE:
    __all__.extend([
        "XRpcWebSocketClient",
        "SubscriptionOptions",
        "Subscription",
        "SubscriptionType",
    ])


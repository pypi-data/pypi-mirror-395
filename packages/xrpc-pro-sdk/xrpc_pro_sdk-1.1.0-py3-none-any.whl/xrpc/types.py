"""
Type definitions and error classes for xRPC SDK
"""

from __future__ import annotations

from typing import Optional, Dict, Any, List, Union, Literal
from dataclasses import dataclass


# Network type - dynamic string type
Network = str

# RPC Type
RpcType = Literal["standard", "beacon", "wss"]


@dataclass
class NetworkInfo:
    """Network information from backend"""

    network: str
    """Network identifier (e.g., 'eth-mainnet')"""

    display_name: str
    """Display name (e.g., 'Ethereum Mainnet')"""

    chain_id: int
    """Chain ID"""

    type: Literal["mainnet", "testnet", "devnet"]
    """Network type"""

    rpc_types: Dict[str, bool]
    """Available RPC types for this network"""

    node_stats: Optional[Dict[str, Any]] = None
    """Node statistics"""

    endpoints: Optional[Dict[str, Optional[str]]] = None
    """Endpoints for each RPC type"""


@dataclass
class ChainInfo:
    """Chain information (group of networks)"""

    id: str
    """Chain identifier (e.g., 'eth', 'polygon')"""

    name: str
    """Chain name (e.g., 'Ethereum')"""

    display_name: str
    """Display name"""

    status: Literal["active", "disabled", "maintenance"]
    """Chain status"""

    subnetworks: List[NetworkInfo]
    """Subnetworks (networks) in this chain"""


@dataclass
class JsonRpcRequest:
    """JSON-RPC 2.0 Request"""

    jsonrpc: str = "2.0"
    method: str = ""
    params: Optional[Union[List[Any], Dict[str, Any]]] = None
    id: Optional[Union[int, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params or [],
            "id": self.id,
        }


@dataclass
class JsonRpcResponse:
    """JSON-RPC 2.0 Response"""

    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JsonRpcResponse":
        """Create from dictionary"""
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            result=data.get("result"),
            error=data.get("error"),
            id=data.get("id"),
        )


@dataclass
class XRpcConfig:
    """xRPC SDK Configuration"""

    api_key: str
    """API Key for authentication"""

    base_url: str = "https://api.xrpc.pro"
    """Base URL of the xRPC API"""

    default_network: Optional[Network] = None
    """Default network to use for requests"""

    timeout: int = 60000
    """Request timeout in milliseconds"""

    debug: bool = False
    """Enable request/response logging"""

    headers: Optional[Dict[str, str]] = None
    """Custom headers to include in requests"""


@dataclass
class RequestOptions:
    """Request options"""

    network: Optional[Network] = None
    """Network to use for this request (overrides default)"""

    timeout: Optional[int] = None
    """Request timeout in milliseconds"""

    skip_cache: bool = False
    """Skip cache for this request"""


@dataclass
class BatchRequestItem:
    """Batch request item"""

    method: str
    params: Optional[Union[List[Any], Dict[str, Any]]] = None
    id: Union[int, str] = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.params or [],
            "id": self.id,
        }


@dataclass
class BatchResponseItem:
    """Batch response item"""

    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchResponseItem":
        """Create from dictionary"""
        return cls(
            jsonrpc=data.get("jsonrpc", "2.0"),
            result=data.get("result"),
            error=data.get("error"),
            id=data.get("id"),
        )


@dataclass
class RequestMetadata:
    """Request metadata"""

    server_latency: Optional[int] = None
    """Server-side latency in milliseconds"""

    timestamp: int = 0
    """Request timestamp"""

    network: Optional[Network] = None
    """Network used"""


class XRpcError(Exception):
    """Error class for xRPC errors"""

    def __init__(
        self, code: int, message: str, data: Optional[Any] = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data
        self.name = "XRpcError"

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return f"XRpcError(code={self.code}, message={self.message!r}, data={self.data})"


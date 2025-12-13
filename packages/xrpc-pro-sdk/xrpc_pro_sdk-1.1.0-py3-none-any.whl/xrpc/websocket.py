"""
WebSocket Client for xRPC - Premium feature

Provides real-time subscriptions via WebSocket Secure (WSS) connections.
Available only for Premium plan users.
"""

import asyncio
import json
import time
from typing import Optional, Dict, Any, List, Callable, Literal
from dataclasses import dataclass

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    from websockets.exceptions import ConnectionClosed
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    WebSocketClientProtocol = None
    ConnectionClosed = Exception

from .types import Network, XRpcError

SubscriptionType = Literal["newHeads", "newPendingTransactions", "logs"]


@dataclass
class SubscriptionOptions:
    """WebSocket subscription options"""

    network: Network
    """Network to use for subscription (use base network name, e.g., 'eth-mainnet', not 'eth-mainnet-wss')"""

    api_key: str
    """API key for authentication"""

    timeout: int = 10000
    """Connection timeout in milliseconds"""

    debug: bool = False
    """Enable debug logging"""

    auto_reconnect: bool = True
    """Auto-reconnect on connection loss"""

    reconnect_delay: int = 5000
    """Reconnect delay in milliseconds"""

    max_reconnect_attempts: int = 0  # 0 = infinite
    """Maximum reconnect attempts (0 = infinite)"""


@dataclass
class Subscription:
    """Active subscription"""

    id: str
    """Subscription ID"""

    type: SubscriptionType
    """Subscription type"""

    params: Optional[List[Any]] = None
    """Parameters used for subscription"""

    callback: Callable[[Any], None] = None
    """Callback function for subscription events"""


class XRpcWebSocketClient:
    """
    WebSocket Client for xRPC subscriptions

    Premium feature - requires Premium plan
    """

    def __init__(self, options: SubscriptionOptions):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets package is required for WebSocket support. "
                "Install it with: pip install websockets"
            )

        if not options.api_key:
            raise ValueError("API key is required")

        if not options.network:
            raise ValueError("Network is required")

        # Note: For WebSocket subscriptions, use the base network name (e.g., 'eth-mainnet')
        # The URL will be constructed as wss://{network}.xrpc.pro
        # Premium plan is required and will be checked by the backend

        self.options = options
        self.ws: Optional[WebSocketClientProtocol] = None
        self.subscriptions: Dict[str, Subscription] = {}
        self.pending_requests: Dict[str | int, Dict[str, Any]] = {}
        self.request_id_counter = 0
        self.reconnect_attempts = 0
        self.is_manual_close = False
        self._reconnect_task: Optional[asyncio.Task] = None
        self._message_handler_task: Optional[asyncio.Task] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def _log(self, *args: Any) -> None:
        """Log message if debug is enabled"""
        if self.options.debug:
            print("[xRPC WebSocket]", *args)

    def _build_websocket_url(self) -> str:
        """Build WebSocket URL"""
        # Remove -wss suffix if present (for HTTP requests network is eth-mainnet-wss,
        # but for WebSocket URL it should be eth-mainnet)
        network_name = self.options.network
        if network_name.endswith("-wss"):
            network_name = network_name[:-4]  # Remove "-wss" suffix
        # Format: wss://{network}.xrpc.pro?apiKey={key}
        # Example: wss://eth-mainnet.xrpc.pro?apiKey=your-key
        return f"wss://{network_name}.xrpc.pro?apiKey={self.options.api_key}"

    async def connect(self) -> None:
        """Connect to WebSocket server"""
        if self.ws and not self.ws.closed:
            self._log("Already connected")
            return

        if not self._loop:
            self._loop = asyncio.get_event_loop()

        url = self._build_websocket_url()
        self._log(f"Connecting to {url}")

        try:
            self.ws = await asyncio.wait_for(
                websockets.connect(url),
                timeout=self.options.timeout / 1000.0,
            )
            self._log("WebSocket connected")
            self.reconnect_attempts = 0

            # Start message handler
            self._message_handler_task = asyncio.create_task(self._handle_messages())
        except asyncio.TimeoutError:
            raise XRpcError(-32603, "WebSocket connection timeout")
        except Exception as e:
            raise XRpcError(-32603, f"WebSocket connection failed: {str(e)}")

    async def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        self.is_manual_close = True

        if self._reconnect_task:
            self._reconnect_task.cancel()
            self._reconnect_task = None

        # Unsubscribe from all subscriptions
        unsubscribe_tasks = []
        for subscription_id in list(self.subscriptions.keys()):
            async def unsubscribe_safe(sub_id: str):
                try:
                    await self.unsubscribe(sub_id)
                except Exception:
                    pass  # Ignore errors during cleanup
            
            unsubscribe_tasks.append(unsubscribe_safe(subscription_id))

        if unsubscribe_tasks:
            await asyncio.gather(*unsubscribe_tasks, return_exceptions=True)

        if self._message_handler_task:
            self._message_handler_task.cancel()
            self._message_handler_task = None

        if self.ws and not self.ws.closed:
            await self.ws.close()

        self.ws = None
        self.subscriptions.clear()
        self.pending_requests.clear()

    async def subscribe_new_heads(
        self, callback: Callable[[Any], None]
    ) -> str:
        """Subscribe to new block headers"""
        return await self.subscribe("newHeads", [], callback)

    async def subscribe_new_pending_transactions(
        self, callback: Callable[[str], None]
    ) -> str:
        """Subscribe to new pending transactions"""
        return await self.subscribe("newPendingTransactions", [], callback)

    async def subscribe_logs(
        self,
        filter_obj: Dict[str, Any],
        callback: Callable[[Any], None],
    ) -> str:
        """Subscribe to logs"""
        return await self.subscribe("logs", [filter_obj], callback)

    async def subscribe(
        self,
        subscription_type: SubscriptionType,
        params: Optional[List[Any]] = None,
        callback: Optional[Callable[[Any], None]] = None,
    ) -> str:
        """Generic subscribe method"""
        if not self.ws or self.ws.closed:
            await self.connect()

        request_id = self._generate_request_id()

        try:
            response = await asyncio.wait_for(
                self._send_request("eth_subscribe", [subscription_type] + (params or []), request_id),
                timeout=self.options.timeout / 1000.0,
            )

            if response.get("error"):
                error = response["error"]
                raise XRpcError(
                    error.get("code", -32603),
                    error.get("message", "Subscription failed"),
                    error.get("data"),
                )

            subscription_id = response.get("result")
            if not subscription_id:
                raise XRpcError(-32603, "Invalid subscription ID received")

            self.subscriptions[subscription_id] = Subscription(
                id=subscription_id,
                type=subscription_type,
                params=params,
                callback=callback,
            )

            self._log(f"Subscribed to {subscription_type} with ID: {subscription_id}")
            return subscription_id

        except asyncio.TimeoutError:
            raise XRpcError(-32603, "Subscribe request timeout")
        except XRpcError:
            raise
        except Exception as e:
            raise XRpcError(-32603, f"Subscribe failed: {str(e)}")

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from a subscription"""
        if subscription_id not in self.subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")

        if not self.ws or self.ws.closed:
            self.subscriptions.pop(subscription_id, None)
            return False

        request_id = self._generate_request_id()

        try:
            response = await asyncio.wait_for(
                self._send_request("eth_unsubscribe", [subscription_id], request_id),
                timeout=self.options.timeout / 1000.0,
            )

            if response.get("error"):
                error = response["error"]
                raise XRpcError(
                    error.get("code", -32603),
                    error.get("message", "Unsubscribe failed"),
                    error.get("data"),
                )

            success = response.get("result") is True
            if success:
                self.subscriptions.pop(subscription_id, None)
                self._log(f"Unsubscribed from {subscription_id}")

            return success

        except asyncio.TimeoutError:
            raise XRpcError(-32603, "Unsubscribe request timeout")
        except XRpcError:
            raise
        except Exception as e:
            raise XRpcError(-32603, f"Unsubscribe failed: {str(e)}")

    def get_state(self) -> str:
        """Get connection state"""
        if not self.ws:
            return "closed"
        if self.ws.closed:
            return "closed"
        return "open"

    def is_connected(self) -> bool:
        """Check if connected"""
        return self.ws is not None and not self.ws.closed

    def get_subscriptions(self) -> List[Subscription]:
        """Get active subscriptions"""
        return list(self.subscriptions.values())

    async def _send_request(
        self, method: str, params: List[Any], request_id: str | int
    ) -> Dict[str, Any]:
        """Send JSON-RPC request"""
        if not self.ws or self.ws.closed:
            raise XRpcError(-32603, "WebSocket is not connected")

        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id,
        }

        self._log(f"Sending request: {method}", request)

        # Create future for response
        future = asyncio.Future()
        self.pending_requests[request_id] = {
            "future": future,
            "timestamp": time.time(),
        }

        try:
            await self.ws.send(json.dumps(request))
            response = await future
            return response
        finally:
            self.pending_requests.pop(request_id, None)

    async def _handle_messages(self) -> None:
        """Handle incoming WebSocket messages"""
        if not self.ws:
            return

        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    self._log("Received message:", data)

                    # Handle subscription events
                    if data.get("method") == "eth_subscription":
                        subscription_id = data.get("params", {}).get("subscription")
                        result = data.get("params", {}).get("result")

                        if subscription_id and subscription_id in self.subscriptions:
                            subscription = self.subscriptions[subscription_id]
                            if subscription.callback:
                                try:
                                    subscription.callback(result)
                                except Exception as e:
                                    self._log(f"Error in subscription callback: {e}")

                        continue

                    # Handle request responses
                    if "id" in data and data["id"] in self.pending_requests:
                        pending = self.pending_requests[data["id"]]
                        pending["future"].set_result(data)

                except json.JSONDecodeError as e:
                    self._log(f"Error parsing message: {e}")
                except Exception as e:
                    self._log(f"Error handling message: {e}")

        except ConnectionClosed:
            self._log("WebSocket connection closed")
            if not self.is_manual_close and self.options.auto_reconnect:
                self._schedule_reconnect()
        except Exception as e:
            self._log(f"Error in message handler: {e}")
            if not self.is_manual_close and self.options.auto_reconnect:
                self._schedule_reconnect()

    def _schedule_reconnect(self) -> None:
        """Schedule reconnection"""
        if (
            self.options.max_reconnect_attempts > 0
            and self.reconnect_attempts >= self.options.max_reconnect_attempts
        ):
            self._log("Max reconnect attempts reached")
            return

        self.reconnect_attempts += 1
        self._log(
            f"Scheduling reconnect attempt {self.reconnect_attempts} "
            f"in {self.options.reconnect_delay}ms"
        )

        async def reconnect():
            await asyncio.sleep(self.options.reconnect_delay / 1000.0)
            try:
                self.is_manual_close = False  # Reset flag for reconnect
                await self.connect()

                # Resubscribe to all subscriptions
                for subscription in list(self.subscriptions.values()):
                    try:
                        new_id = await self.subscribe(
                            subscription.type,
                            subscription.params,
                            subscription.callback,
                        )
                        # Remove old subscription ID
                        if new_id != subscription.id:
                            self.subscriptions.pop(subscription.id, None)
                    except Exception as e:
                        self._log(f"Failed to resubscribe {subscription.id}: {e}")

            except Exception as e:
                self._log(f"Reconnect failed: {e}")
                if not self.is_manual_close:
                    self._schedule_reconnect()

        if self._loop:
            self._reconnect_task = asyncio.create_task(reconnect())

    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        self.request_id_counter += 1
        return f"{int(time.time() * 1000)}-{self.request_id_counter}-{''.join(__import__('random').choices(__import__('string').ascii_lowercase + __import__('string').digits, k=7))}"


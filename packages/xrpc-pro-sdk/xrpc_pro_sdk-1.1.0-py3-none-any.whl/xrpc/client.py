"""
xRPC Client - Main SDK class
"""

import time
import random
import string
from typing import Optional, Dict, Any, List, Tuple, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .types import (
    Network,
    JsonRpcRequest,
    JsonRpcResponse,
    XRpcConfig,
    RequestOptions,
    BatchRequestItem,
    BatchResponseItem,
    RequestMetadata,
    ChainInfo,
    NetworkInfo,
    XRpcError,
)


class XRpcClient:
    """xRPC Client - Main SDK class"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_network: Optional[Network] = None,
        timeout: int = 60000,
        debug: bool = False,
        headers: Optional[Dict[str, str]] = None,
        config: Optional[XRpcConfig] = None,
    ):
        """
        Initialize xRPC client.

        Can be initialized either with individual parameters or with XRpcConfig object.

        Args:
            api_key: API key for authentication (required if config not provided)
            base_url: Base URL of the xRPC API (default: https://api.xrpc.pro)
            default_network: Default network for requests
            timeout: Request timeout in milliseconds (default: 60000)
            debug: Enable request/response logging (default: False)
            headers: Custom headers to include in requests
            config: XRpcConfig object (alternative to individual parameters)
        """
        # Support both config object and individual parameters
        if config:
            api_key = config.api_key
            base_url = config.base_url
            default_network = config.default_network
            timeout = config.timeout
            debug = config.debug
            headers = config.headers

        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.base_url = base_url or "https://api.xrpc.pro"
        self.default_network = default_network
        self.timeout = timeout / 1000.0  # Convert ms to seconds
        self.debug = debug

        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
        )

        if headers:
            self.session.headers.update(headers)

    def _log(self, message: str) -> None:
        """Log message if debug is enabled"""
        if self.debug:
            print(f"[xRPC] {message}")

    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        return f"{int(time.time() * 1000)}{''.join(random.choices(string.ascii_lowercase + string.digits, k=7))}"

    def request(
        self,
        method: str,
        params: Optional[Union[List[Any], Dict[str, Any]]] = None,
        options: Optional[RequestOptions] = None,
    ) -> Tuple[Any, RequestMetadata]:
        """
        Make a single RPC request

        Args:
            method: RPC method name
            params: Method parameters
            options: Request options

        Returns:
            Tuple of (result, metadata)

        Raises:
            XRpcError: If request fails
        """
        network = options.network if options and options.network else self.default_network

        if not network:
            raise ValueError(
                "Network is required. Provide it in options or set default_network in config."
            )

        request_id = self._generate_request_id()
        request_body: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": request_id,
        }

        start_time = int(time.time() * 1000)

        try:
            url = f"{self.base_url}/rpc/{network}"
            timeout = (
                (options.timeout / 1000.0 if options and options.timeout else None)
                or self.timeout
            )

            self._log(f"Request: POST {url} {request_body}")

            response = self.session.post(url, json=request_body, timeout=timeout)

            self._log(
                f"Response: {response.status_code} {response.headers.get('x-server-latency', 'N/A')}ms {response.text[:200]}"
            )

            server_latency = None
            if "x-server-latency" in response.headers:
                try:
                    server_latency = int(response.headers["x-server-latency"])
                except (ValueError, TypeError):
                    pass

            metadata = RequestMetadata(
                server_latency=server_latency,
                timestamp=start_time,
                network=network,
            )

            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                json_response = JsonRpcResponse.from_dict(data)

                if json_response.error:
                    raise XRpcError(
                        json_response.error.get("code", -32603),
                        json_response.error.get("message", "Unknown error"),
                        json_response.error.get("data"),
                    )

                if json_response.result is None:
                    raise XRpcError(-32603, "Response missing result")

                return json_response.result, metadata

            raise XRpcError(-32603, "Invalid response format")

        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status_code = e.response.status_code
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict) and "error" in error_data:
                        error = error_data["error"]
                        raise XRpcError(
                            error.get("code", -32603),
                            error.get("message", "Unknown error"),
                            error.get("data"),
                        )
                except (ValueError, KeyError):
                    pass

                if status_code == 401:
                    raise XRpcError(-32601, "Invalid API key")
                elif status_code == 403:
                    raise XRpcError(
                        -32601,
                        "Access denied. Premium plan required for this network type.",
                    )
                elif status_code == 429:
                    raise XRpcError(-32601, "Rate limit exceeded")

            raise XRpcError(-32603, f"HTTP error: {str(e)}")

        except requests.exceptions.Timeout:
            raise XRpcError(-32603, "Request timeout")

        except requests.exceptions.RequestException as e:
            raise XRpcError(-32603, f"Network error: {str(e)}")

        except XRpcError:
            raise

        except Exception as e:
            raise XRpcError(-32603, f"Unknown error: {str(e)}")

    def batch(
        self,
        requests: List[BatchRequestItem],
        options: Optional[RequestOptions] = None,
    ) -> Tuple[List[BatchResponseItem], RequestMetadata]:
        """
        Make a batch RPC request

        Args:
            requests: List of batch request items
            options: Request options

        Returns:
            Tuple of (results, metadata)

        Raises:
            XRpcError: If request fails
        """
        network = options.network if options and options.network else self.default_network

        if not network:
            raise ValueError(
                "Network is required. Provide it in options or set default_network in config."
            )

        if not requests:
            raise ValueError("Batch request must contain at least one request")

        request_body = [req.to_dict() for req in requests]

        start_time = int(time.time() * 1000)

        try:
            url = f"{self.base_url}/rpc/{network}"
            timeout = (
                (options.timeout / 1000.0 if options and options.timeout else None)
                or self.timeout
            )

            self._log(f"Batch Request: POST {url} {len(request_body)} requests")

            response = self.session.post(url, json=request_body, timeout=timeout)

            self._log(
                f"Batch Response: {response.status_code} {response.headers.get('x-server-latency', 'N/A')}ms"
            )

            server_latency = None
            if "x-server-latency" in response.headers:
                try:
                    server_latency = int(response.headers["x-server-latency"])
                except (ValueError, TypeError):
                    pass

            metadata = RequestMetadata(
                server_latency=server_latency,
                timestamp=start_time,
                network=network,
            )

            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                results = [
                    BatchResponseItem.from_dict(item) for item in data
                ]
                return results, metadata

            raise XRpcError(-32603, "Invalid batch response format")

        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict) and "error" in error_data:
                        error = error_data["error"]
                        raise XRpcError(
                            error.get("code", -32603),
                            error.get("message", "Unknown error"),
                            error.get("data"),
                        )
                except (ValueError, KeyError):
                    pass

            raise XRpcError(-32603, f"HTTP error: {str(e)}")

        except requests.exceptions.Timeout:
            raise XRpcError(-32603, "Request timeout")

        except requests.exceptions.RequestException as e:
            raise XRpcError(-32603, f"Network error: {str(e)}")

        except XRpcError:
            raise

        except Exception as e:
            raise XRpcError(-32603, f"Unknown error: {str(e)}")

    def health(self) -> Dict[str, Any]:
        """
        Get health status

        Returns:
            Health status dictionary

        Raises:
            XRpcError: If request fails
        """
        try:
            url = f"{self.base_url}/rpc/health"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise XRpcError(-32603, f"Health check failed: {str(e)}")

    def get_available_networks(self) -> List[ChainInfo]:
        """
        Get available networks

        Returns:
            List of chain information

        Raises:
            XRpcError: If request fails
        """
        try:
            url = f"{self.base_url}/chains"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and data.get("success") and data.get("data"):
                chains = []
                for chain_data in data["data"]:
                    subnetworks = []
                    for subnetwork_data in chain_data.get("subnetworks", []):
                        subnetworks.append(
                            NetworkInfo(
                                network=subnetwork_data["network"],
                                display_name=subnetwork_data["displayName"],
                                chain_id=subnetwork_data["chainId"],
                                type=subnetwork_data["type"],
                                rpc_types=subnetwork_data.get("rpcTypes", {}),
                                node_stats=subnetwork_data.get("nodeStats"),
                                endpoints=subnetwork_data.get("endpoints"),
                            )
                        )
                    chains.append(
                        ChainInfo(
                            id=chain_data["id"],
                            name=chain_data["name"],
                            display_name=chain_data["displayName"],
                            status=chain_data["status"],
                            subnetworks=subnetworks,
                        )
                    )
                return chains

            raise XRpcError(-32603, "Failed to fetch networks")

        except requests.exceptions.RequestException as e:
            raise XRpcError(-32603, f"Failed to fetch networks: {str(e)}")

    def get_network_stats(self) -> Dict[str, int]:
        """
        Get network statistics

        Returns:
            Network statistics dictionary

        Raises:
            XRpcError: If request fails
        """
        try:
            url = f"{self.base_url}/chains/stats"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and data.get("success") and data.get("data"):
                return data["data"]

            raise XRpcError(-32603, "Failed to fetch network stats")

        except requests.exceptions.RequestException as e:
            raise XRpcError(-32603, f"Failed to fetch network stats: {str(e)}")

    def set_api_key(self, api_key: str) -> None:
        """
        Update API key

        Args:
            api_key: New API key
        """
        if not api_key:
            raise ValueError("API key cannot be empty")
        self.api_key = api_key
        self.session.headers["X-API-Key"] = api_key

    def set_default_network(self, network: Network) -> None:
        """
        Update default network

        Args:
            network: Network identifier
        """
        self.default_network = network

    def get_api_key(self) -> str:
        """
        Get current API key (masked)

        Returns:
            Masked API key (first 8 characters + "...")
        """
        if self.api_key:
            return f"{self.api_key[:8]}..."
        return ""


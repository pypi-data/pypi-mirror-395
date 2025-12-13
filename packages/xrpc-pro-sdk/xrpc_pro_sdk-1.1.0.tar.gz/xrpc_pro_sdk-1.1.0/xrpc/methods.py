"""
Convenience methods for common RPC calls
"""

from typing import Optional, Dict, Any, List
from .client import XRpcClient
from .types import RequestOptions


class XRpcClientExtended(XRpcClient):
    """Extended client with convenience methods"""

    def get_block_number(
        self, options: Optional[RequestOptions] = None
    ) -> str:
        """Get current block number"""
        result, _ = self.request("eth_blockNumber", [], options)
        return result

    def get_balance(
        self,
        address: str,
        block_tag: str = "latest",
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Get balance of an address"""
        result, _ = self.request("eth_getBalance", [address, block_tag], options)
        return result

    def get_transaction_count(
        self,
        address: str,
        block_tag: str = "latest",
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Get transaction count (nonce) for an address"""
        result, _ = self.request(
            "eth_getTransactionCount", [address, block_tag], options
        )
        return result

    def get_gas_price(
        self, options: Optional[RequestOptions] = None
    ) -> str:
        """Get gas price"""
        result, _ = self.request("eth_gasPrice", [], options)
        return result

    def get_transaction_receipt(
        self, tx_hash: str, options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """Get transaction receipt"""
        result, _ = self.request("eth_getTransactionReceipt", [tx_hash], options)
        return result

    def get_transaction(
        self, tx_hash: str, options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """Get transaction by hash"""
        result, _ = self.request("eth_getTransactionByHash", [tx_hash], options)
        return result

    def get_block_by_number(
        self,
        block_number: str,
        full_transactions: bool = False,
        options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """Get block by number"""
        result, _ = self.request(
            "eth_getBlockByNumber", [block_number, full_transactions], options
        )
        return result

    def get_block_by_hash(
        self,
        block_hash: str,
        full_transactions: bool = False,
        options: Optional[RequestOptions] = None,
    ) -> Dict[str, Any]:
        """Get block by hash"""
        result, _ = self.request(
            "eth_getBlockByHash", [block_hash, full_transactions], options
        )
        return result

    def call(
        self,
        call_object: Dict[str, Any],
        block_tag: str = "latest",
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Call a contract method"""
        result, _ = self.request("eth_call", [call_object, block_tag], options)
        return result

    def estimate_gas(
        self,
        transaction: Dict[str, Any],
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Estimate gas for a transaction"""
        result, _ = self.request("eth_estimateGas", [transaction], options)
        return result

    def send_raw_transaction(
        self, signed_tx: str, options: Optional[RequestOptions] = None
    ) -> str:
        """Send raw transaction"""
        result, _ = self.request("eth_sendRawTransaction", [signed_tx], options)
        return result

    def get_logs(
        self,
        filter_obj: Dict[str, Any],
        options: Optional[RequestOptions] = None,
    ) -> List[Dict[str, Any]]:
        """Get logs"""
        result, _ = self.request("eth_getLogs", [filter_obj], options)
        return result

    def get_code(
        self,
        address: str,
        block_tag: str = "latest",
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Get code at address"""
        result, _ = self.request("eth_getCode", [address, block_tag], options)
        return result

    def get_storage_at(
        self,
        address: str,
        position: str,
        block_tag: str = "latest",
        options: Optional[RequestOptions] = None,
    ) -> str:
        """Get storage at address"""
        result, _ = self.request(
            "eth_getStorageAt", [address, position, block_tag], options
        )
        return result

    def get_chain_id(
        self, options: Optional[RequestOptions] = None
    ) -> str:
        """Get chain ID"""
        result, _ = self.request("eth_chainId", [], options)
        return result

    def get_network_version(
        self, options: Optional[RequestOptions] = None
    ) -> str:
        """Get network version"""
        result, _ = self.request("net_version", [], options)
        return result


"""
Basic usage example
"""

from xrpc import XRpcClient

def main():
    # Initialize client with individual parameters
    client = XRpcClient(
        api_key="your-api-key-here",
        default_network="eth-mainnet",
        debug=True
    )
    
    # Alternative: Initialize with config object
    # from xrpc import XRpcConfig
    # config = XRpcConfig(
    #     api_key="your-api-key-here",
    #     default_network="eth-mainnet",
    #     debug=True
    # )
    # client = XRpcClient(config=config)

    try:
        # Get current block number
        result, metadata = client.request("eth_blockNumber")
        print(f"Current block: {result}")
        print(f"Server latency: {metadata.server_latency} ms")

        # Get balance
        result, _ = client.request(
            "eth_getBalance",
            ["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "latest"]
        )
        print(f"Balance: {result}")

        # Get gas price
        result, _ = client.request("eth_gasPrice")
        print(f"Gas price: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


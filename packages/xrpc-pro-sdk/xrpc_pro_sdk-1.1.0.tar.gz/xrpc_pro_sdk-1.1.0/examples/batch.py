"""
Batch request example
"""

from xrpc import XRpcClient, BatchRequestItem

def main():
    client = XRpcClient(
        api_key="your-api-key-here",
        default_network="eth-mainnet"
    )

    try:
        # Create batch requests
        requests = [
            BatchRequestItem(method="eth_blockNumber", params=[], id=1),
            BatchRequestItem(method="eth_gasPrice", params=[], id=2),
            BatchRequestItem(
                method="eth_getBalance",
                params=["0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "latest"],
                id=3
            )
        ]

        # Execute batch request
        results, metadata = client.batch(requests)

        # Process results
        for response in results:
            if response.error:
                print(f"Error: {response.error}")
            else:
                print(f"Result: {response.result}")

        print(f"Server latency: {metadata.server_latency} ms")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


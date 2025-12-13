"""
Convenience methods example
"""

from xrpc import XRpcClientExtended

def main():
    client = XRpcClientExtended(
        api_key="your-api-key-here",
        default_network="eth-mainnet"
    )

    try:
        # Use convenience methods
        block_number = client.get_block_number()
        print(f"Block number: {block_number}")

        balance = client.get_balance("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
        print(f"Balance: {balance}")

        gas_price = client.get_gas_price()
        print(f"Gas price: {gas_price}")

        # Different network
        from xrpc import RequestOptions
        polygon_block = client.get_block_number(
            RequestOptions(network="polygon-mainnet")
        )
        print(f"Polygon block: {polygon_block}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


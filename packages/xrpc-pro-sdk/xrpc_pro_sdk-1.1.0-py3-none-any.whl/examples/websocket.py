"""
WebSocket subscriptions example

Premium feature - requires Premium plan
"""

import asyncio
from xrpc import XRpcWebSocketClient, SubscriptionOptions

async def main():
    # Create WebSocket client
    options = SubscriptionOptions(
        api_key="your-api-key-here",
        network="eth-mainnet",  # Use base network name (not eth-mainnet-wss)
        debug=True,
        auto_reconnect=True,
    )
    
    ws_client = XRpcWebSocketClient(options)

    try:
        # Connect to WebSocket
        await ws_client.connect()
        print("Connected!")

        # Subscribe to new block headers
        new_heads_sub = await ws_client.subscribe_new_heads(
            lambda block: print(f"New block: {block}")
        )
        print(f"Subscribed to newHeads: {new_heads_sub}")

        # Subscribe to new pending transactions
        pending_tx_sub = await ws_client.subscribe_new_pending_transactions(
            lambda tx_hash: print(f"New pending transaction: {tx_hash}")
        )
        print(f"Subscribed to newPendingTransactions: {pending_tx_sub}")

        # Subscribe to logs
        logs_sub = await ws_client.subscribe_logs(
            {
                "address": "0x...",  # Contract address
                "topics": ["0x..."],  # Event topics
            },
            lambda log: print(f"New log: {log}")
        )
        print(f"Subscribed to logs: {logs_sub}")

        # Keep connection alive
        # In a real application, you would handle cleanup on exit
        await asyncio.sleep(3600)  # Run for 1 hour

    except KeyboardInterrupt:
        print("Disconnecting...")
    finally:
        await ws_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())


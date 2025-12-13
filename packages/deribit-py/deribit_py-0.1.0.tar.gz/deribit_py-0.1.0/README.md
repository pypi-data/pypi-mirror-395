# Deribit Options Client

A complete, async Python client for the Deribit Options Market, supporting both REST and WebSocket protocols.

## Features

- **Asyncio-native**: Built on `aiohttp` and `websockets`.
- **Dual Protocol**: Seamlessly use REST for one-off requests and WebSockets for streaming.
- **Unified Client**: Access both `rest` and `ws` interfaces through a single `DeribitClient`.
- **Authentication**: Supports Client Credentials flow for private endpoints.
- **Generic Support**: Helper methods for common actions (Buy, Sell, Get Instruments), plus generic `public_request`, `private_request`, and `send_request` methods to access *any* Deribit endpoint.

## Installation

```bash
pip install .
```

(Or install dependencies manually: `pip install aiohttp websockets`)

## Usage

### Initialization

```python
from deribit import DeribitClient

# For Testnet, set testnet=True
client = DeribitClient(client_id="YOUR_ID", client_secret="YOUR_SECRET", testnet=False)
```

### REST API

```python
# Public
instruments = await client.rest.get_instruments("BTC")

# Private (auto-authenticates)
positions = await client.rest.get_positions("BTC")
buy_order = await client.rest.buy("BTC-29MAR24-50000-C", 1.0, price=0.05)
```

### WebSocket API

```python
await client.ws.connect()

def on_message(data):
    print(data)

# Subscribe with callback
await client.ws.subscribe(["trades.BTC-PERPETUAL.100ms"], on_message)

# Send request via WS
instruments = await client.ws.get_instruments("BTC")
```

### Generic Requests

If a specific method wrapper is missing, you can call any endpoint directly:

```python
# REST
res = await client.rest.private_request("private/get_user_trades_by_currency", {"currency": "BTC"})

# WebSocket
res = await client.ws.send_request("private/get_user_trades_by_currency", {"currency": "BTC"})
```

## Structure

- `deribit.rest`: Handles HTTP requests, session management, and token refresh.
- `deribit.ws`: Handles persistent WebSocket connection, subscription management, and request/response correlation.


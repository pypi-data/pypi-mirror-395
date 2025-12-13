import asyncio
import websockets
import json
import logging
from typing import Optional, Dict, Any, Callable, List

logger = logging.getLogger(__name__)

class DeribitWS:
    URL_PROD = "wss://www.deribit.com/ws/api/v2"
    URL_TEST = "wss://test.deribit.com/ws/api/v2"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, testnet=False):
        self.url = self.URL_TEST if testnet else self.URL_PROD
        self.client_id = client_id
        self.client_secret = client_secret
        
        self.ws = None
        self.msg_id = 0
        self.futures = {} # Map msg_id -> Future
        self.subscriptions = {} # Map channel -> callback
        self.running = False

    async def connect(self):
        self.ws = await websockets.connect(self.url, max_size=2**20 * 10) # 10MB limit
        self.running = True
        logger.info(f"Connected to {self.url}")
        
        # Start listening loop in background
        asyncio.create_task(self._listen())

        # Authenticate if credentials provided
        if self.client_id and self.client_secret:
            await self.authenticate()

    async def authenticate(self):
        logger.info("Authenticating WebSocket...")
        msg = {
            "jsonrpc": "2.0",
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        }
        await self.send_request(msg["method"], msg["params"])
        logger.info("WebSocket Authenticated.")

    async def _listen(self):
        try:
            async for message in self.ws:
                data = json.loads(message)
                
                # Handle Subscription Updates
                if "method" in data and data["method"] == "subscription":
                    params = data["params"]
                    channel = params["channel"]
                    if channel in self.subscriptions:
                        try:
                            # Call the callback registered for this channel
                            cb = self.subscriptions[channel]
                            if asyncio.iscoroutinefunction(cb):
                                await cb(params["data"])
                            else:
                                cb(params["data"])
                        except Exception as e:
                            logger.error(f"Error in callback for {channel}: {e}")
                
                # Handle Request Responses
                elif "id" in data and data["id"] in self.futures:
                    fut = self.futures.pop(data["id"])
                    if "error" in data:
                        fut.set_exception(Exception(data["error"]))
                    else:
                        fut.set_result(data.get("result"))
                
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            self.running = False

    async def send_request(self, method: str, params: Dict[str, Any] = None):
        if not self.ws or not self.running:
            raise Exception("WebSocket not connected.")

        self.msg_id += 1
        current_id = self.msg_id
        
        # Filter None params
        if params:
             new_params = {}
             for k, v in params.items():
                 if v is None:
                     continue
                 if isinstance(v, bool):
                     new_params[k] = "true" if v else "false"
                 else:
                     new_params[k] = v
             params = new_params
        
        msg = {
            "jsonrpc": "2.0",
            "id": current_id,
            "method": method,
            "params": params or {}
        }
        
        # Create future to wait for response
        fut = asyncio.get_running_loop().create_future()
        self.futures[current_id] = fut
        
        await self.ws.send(json.dumps(msg))
        return await fut

    async def subscribe(self, channels: List[str], callback: Callable):
        """
        Subscribe to a list of channels and register a callback for them.
        """
        # Register callback locally
        for ch in channels:
            self.subscriptions[ch] = callback

        # Send subscription request
        res = await self.send_request("public/subscribe", {"channels": channels})
        return res

    async def unsubscribe(self, channels: List[str]):
        res = await self.send_request("public/unsubscribe", {"channels": channels})
        for ch in channels:
            if ch in self.subscriptions:
                del self.subscriptions[ch]
        return res
    
    async def unsubscribe_all(self):
         res = await self.send_request("public/unsubscribe_all")
         self.subscriptions.clear()
         return res

    async def close(self):
        self.running = False
        if self.ws:
            await self.ws.close()

    # --- Helper Wrappers ---
    # WebSocket also allows request-response access to many endpoints normally associated with REST
    
    async def get_time(self):
        return await self.send_request("public/get_time")

    async def get_instruments(self, currency: str, kind: str = "option", expired: bool = False):
        return await self.send_request("public/get_instruments", {"currency": currency, "kind": kind, "expired": expired})

    async def get_order_book(self, instrument_name: str, depth: int = None):
        return await self.send_request("public/get_order_book", {"instrument_name": instrument_name, "depth": depth})

    async def get_ticker(self, instrument_name: str):
        return await self.send_request("public/ticker", {"instrument_name": instrument_name})
    
    async def get_user_trades_by_instrument(self, instrument_name: str, count: int = None):
        return await self.send_request("private/get_user_trades_by_instrument", {"instrument_name": instrument_name, "count": count})
    
    async def get_positions(self, currency: str, kind: str = "option"):
        return await self.send_request("private/get_positions", {"currency": currency, "kind": kind})

    async def buy(self, instrument_name: str, amount: float, type: str = "limit", price: float = None):
        params = {"instrument_name": instrument_name, "amount": amount, "type": type}
        if price: params["price"] = price
        return await self.send_request("private/buy", params)

    async def sell(self, instrument_name: str, amount: float, type: str = "limit", price: float = None):
        params = {"instrument_name": instrument_name, "amount": amount, "type": type}
        if price: params["price"] = price
        return await self.send_request("private/sell", params)

    async def cancel(self, order_id: str):
        return await self.send_request("private/cancel", {"order_id": order_id})

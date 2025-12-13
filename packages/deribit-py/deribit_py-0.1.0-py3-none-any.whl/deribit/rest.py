import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class DeribitREST:
    BASE_URL = "https://www.deribit.com/api/v2"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, testnet=False):
        self.client_id = client_id
        self.client_secret = client_secret
        if testnet:
            self.BASE_URL = "https://test.deribit.com/api/v2"
        
        self.session = None
        self.access_token = None
        self.refresh_token = None

    async def _get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()

    async def authenticate(self):
        """
        Obtain an access token using client credentials.
        """
        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and Secret required for authentication.")

        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = await self.public_request("public/auth", params)
        if "result" in response:
            self.access_token = response["result"]["access_token"]
            self.refresh_token = response["result"]["refresh_token"]
            logger.info("REST Authentication successful.")
        else:
            raise Exception(f"Authentication failed: {response}")

    async def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None, private: bool = False):
        session = await self._get_session()
        url = f"{self.BASE_URL}/{endpoint}"
        
        headers = {}
        if private:
            if not self.access_token:
                await self.authenticate()
            headers["Authorization"] = f"Bearer {self.access_token}"

        # Filter None params and convert booleans to lowercase strings
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

        async with session.get(url, params=params, headers=headers) as resp:
            data = await resp.json()
            if "error" in data:
                logger.error(f"API Error {endpoint}: {data['error']}")
                raise Exception(f"Deribit API Error: {data['error']}")
            return data["result"]

    async def public_request(self, endpoint: str, params: Dict[str, Any] = None):
        return await self._request("GET", endpoint, params, private=False)

    async def private_request(self, endpoint: str, params: Dict[str, Any] = None):
        return await self._request("GET", endpoint, params, private=True)

    # --- Market Data (Public) ---

    async def get_time(self):
        return await self.public_request("public/get_time")

    async def get_instruments(self, currency: str, kind: str = "option", expired: bool = False):
        return await self.public_request("public/get_instruments", {
            "currency": currency,
            "kind": kind,
            "expired": expired
        })

    async def get_book_summary_by_currency(self, currency: str, kind: str = "option"):
        """
        Retrieves the book summary (ticker info) for all instruments in the currency.
        Includes Greeks like delta, gamma, vega, theta, rho for options.
        """
        return await self.public_request("public/get_book_summary_by_currency", {
            "currency": currency,
            "kind": kind
        })

    async def get_order_book(self, instrument_name: str, depth: int = None):
        """
        Retrieves the order book for a specific instrument.
        Includes bid/ask greeks in some contexts, but primarily price/amount.
        """
        return await self.public_request("public/get_order_book", {
            "instrument_name": instrument_name,
            "depth": depth
        })

    async def get_last_trades_by_instrument(self, instrument_name: str, count: int = None, start_seq: int = None, end_seq: int = None):
        return await self.public_request("public/get_last_trades_by_instrument", {
            "instrument_name": instrument_name,
            "count": count,
            "start_seq": start_seq,
            "end_seq": end_seq
        })
    
    async def get_last_trades_by_currency(self, currency: str, kind: str = "option", count: int = None):
         return await self.public_request("public/get_last_trades_by_currency", {
            "currency": currency,
            "kind": kind,
            "count": count
        })

    async def get_ticker(self, instrument_name: str):
         """
         Get ticker for an instrument, including greeks, best bid/ask, mark price, etc.
         """
         return await self.public_request("public/ticker", {
            "instrument_name": instrument_name
        })
    
    async def get_historical_volatility(self, currency: str):
        return await self.public_request("public/get_historical_volatility", {
            "currency": currency
        })

    # --- Trading & Account (Private) ---

    async def get_positions(self, currency: str, kind: str = "option"):
        return await self.private_request("private/get_positions", {
            "currency": currency,
            "kind": kind
        })

    async def get_open_orders_by_currency(self, currency: str, kind: str = "option"):
        return await self.private_request("private/get_open_orders_by_currency", {
            "currency": currency,
            "kind": kind
        })

    async def get_open_orders_by_instrument(self, instrument_name: str):
        return await self.private_request("private/get_open_orders_by_instrument", {
            "instrument_name": instrument_name
        })

    async def get_user_trades_by_currency(self, currency: str, kind: str = "option", count: int = None):
        return await self.private_request("private/get_user_trades_by_currency", {
            "currency": currency,
            "kind": kind,
            "count": count
        })

    async def get_user_trades_by_instrument(self, instrument_name: str, count: int = None):
        return await self.private_request("private/get_user_trades_by_instrument", {
            "instrument_name": instrument_name,
            "count": count
        })

    async def get_settlement_history_by_instrument(self, instrument_name: str, count: int = None):
        return await self.private_request("private/get_settlement_history_by_instrument", {
            "instrument_name": instrument_name,
            "count": count
        })

    async def get_settlement_history_by_currency(self, currency: str, kind: str = "option", count: int = None):
        return await self.private_request("private/get_settlement_history_by_currency", {
            "currency": currency,
            "kind": kind,
            "count": count
        })

    async def buy(self, instrument_name: str, amount: float, type: str = "limit", price: float = None, label: str = None, time_in_force: str = "good_till_cancelled", post_only: bool = False, reduce_only: bool = False):
        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": type,
            "label": label,
            "time_in_force": time_in_force,
            "post_only": post_only,
            "reduce_only": reduce_only
        }
        if price:
            params["price"] = price
        return await self.private_request("private/buy", params)

    async def sell(self, instrument_name: str, amount: float, type: str = "limit", price: float = None, label: str = None, time_in_force: str = "good_till_cancelled", post_only: bool = False, reduce_only: bool = False):
        params = {
            "instrument_name": instrument_name,
            "amount": amount,
            "type": type,
            "label": label,
            "time_in_force": time_in_force,
            "post_only": post_only,
            "reduce_only": reduce_only
        }
        if price:
            params["price"] = price
        return await self.private_request("private/sell", params)
    
    async def edit(self, order_id: str, amount: float, price: float):
        return await self.private_request("private/edit", {
            "order_id": order_id,
            "amount": amount,
            "price": price
        })

    async def cancel(self, order_id: str):
        return await self.private_request("private/cancel", {
            "order_id": order_id
        })

    async def cancel_all(self):
        return await self.private_request("private/cancel_all")

    async def cancel_all_by_currency(self, currency: str, kind: str = "option"):
        return await self.private_request("private/cancel_all_by_currency", {
            "currency": currency,
            "kind": kind
        })

    async def get_account_summary(self, currency: str, extended: bool = True):
        return await self.private_request("private/get_account_summary", {
            "currency": currency,
            "extended": extended
        })
    
    async def get_subaccounts(self, with_portfolio: bool = False):
        return await self.private_request("private/get_subaccounts", {
            "with_portfolio": with_portfolio
        })

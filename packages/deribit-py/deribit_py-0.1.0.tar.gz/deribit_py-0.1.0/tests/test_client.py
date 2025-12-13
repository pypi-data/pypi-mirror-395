import unittest
import asyncio
from deribit import DeribitClient

class TestDeribitClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Using generic public endpoints, no auth required for these
        self.client = DeribitClient(testnet=False)

    async def asyncTearDown(self):
        await self.client.close()

    async def test_rest_public_get_time(self):
        """Test public REST connectivity."""
        res = await self.client.rest.get_time()
        # API returns the timestamp directly as an integer in 'result'
        self.assertIsInstance(res, int)

    async def test_rest_get_instruments(self):
        """Test fetching instruments via REST."""
        res = await self.client.rest.get_instruments("BTC")
        self.assertIsInstance(res, list)
        if len(res) > 0:
            self.assertIn("instrument_name", res[0])

    async def test_rest_get_order_book(self):
        """Test fetching order book for a specific instrument."""
        # Need a valid instrument. Let's fetch one first.
        insts = await self.client.rest.get_instruments("BTC")
        if not insts:
            self.skipTest("No instruments found")
        
        target = insts[0]["instrument_name"]
        book = await self.client.rest.get_order_book(target)
        self.assertIn("bids", book)
        self.assertIn("asks", book)

    async def test_ws_connect_and_request(self):
        """Test WebSocket connectivity and request-response."""
        await self.client.ws.connect()
        res = await self.client.ws.get_time()
        self.assertIsInstance(res, int)

    async def test_ws_get_instruments(self):
         """Test WebSocket instrument fetching."""
         await self.client.ws.connect()
         res = await self.client.ws.get_instruments("BTC")
         self.assertIsInstance(res, list)

if __name__ == '__main__':
    unittest.main()

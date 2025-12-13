from .rest import DeribitREST
from .ws import DeribitWS

class DeribitClient:
    """
    Unified client for Deribit.
    """
    def __init__(self, client_id=None, client_secret=None, testnet=False):
        self.rest = DeribitREST(client_id, client_secret, testnet)
        self.ws = DeribitWS(client_id, client_secret, testnet)

    async def close(self):
        await self.rest.close()
        await self.ws.close()


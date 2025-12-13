import asyncio
from typing import Awaitable, Callable, Optional

from pymacaroons2.macaroon import Macaroon
from pymacaroons2.verifier import Verifier


class AsyncVerifier(Verifier):
    def __init__(
        self, caveat_fetcher: Optional[Callable[[bytes], Awaitable[bytes]]] = None
    ):
        super().__init__()
        self._caveat_fetcher = caveat_fetcher

    async def verify_async(self, macaroon: Macaroon, key: bytes):
        # Simple async wrapper
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.verify, macaroon, key)

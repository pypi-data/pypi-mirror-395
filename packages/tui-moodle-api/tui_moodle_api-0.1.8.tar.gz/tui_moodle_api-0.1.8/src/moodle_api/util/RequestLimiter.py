import asyncio
from asyncio import Lock
from time import time


class RequestLimiter:
    def __init__(self, wait_time: float):
        self._lock: Lock = Lock()
        self._wait_time: float = wait_time
        self._last_request: float = 0.0

    async def __aenter__(self):
        await self._lock.__aenter__()

        diff = self._last_request + self._wait_time - time()
        if diff > 0:
            await asyncio.sleep(diff)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._last_request = time()
        await self._lock.__aexit__(exc_type, exc_val, exc_tb)

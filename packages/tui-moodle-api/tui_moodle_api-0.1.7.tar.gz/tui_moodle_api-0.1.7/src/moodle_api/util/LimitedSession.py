import asyncio
import logging
from typing import Any

from aiohttp import ClientSession, ClientResponse, TCPConnector, client_exceptions
from bs4 import BeautifulSoup
from yarl import URL

from .RequestLimiter import RequestLimiter


class LimitedSession:
    def __init__(self, host: str, wait_time: float):
        # initialize session
        connector = TCPConnector(
            limit=5,
            limit_per_host=1
        )

        self._session = ClientSession(connector=connector)

        # store other properties
        self.host: str = host
        self._limiter: RequestLimiter = RequestLimiter(wait_time)

    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    def _url(self, path: str):
        if path.startswith('https://') or path.startswith('http://'):
            return path
        elif path.startswith('/'):
            return f'{self.host}{path}'
        else:
            return f'{self.host}/{path}'

    @staticmethod
    async def _parse(response: ClientResponse) -> BeautifulSoup:
        return BeautifulSoup((await response.read()).decode('utf-8'), 'html.parser')

    async def get_html(self, path: str) -> BeautifulSoup:
        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.get(self._url(path)) as response:
                        return await self._parse(response)
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

    async def get_html_redirects(self, path: str) -> tuple[BeautifulSoup, list[tuple[int, URL]]]:
        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.get(self._url(path)) as response:
                        return (
                            await self._parse(response),
                            [(h.status, h.url) for h in response.history] + [(response.status, response.url)]
                        )
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

    async def get_json(self, path: str) -> dict | list:
        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.get(self._url(path)) as response:
                        return await response.json()
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

    async def get_bytes(self, path: str) -> bytes:
        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.get(self._url(path)) as response:
                        return await response.read()
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

    async def post_html(self, path: str, data: dict[str, Any]) -> BeautifulSoup:
        for key in data:
            if not isinstance(data[key], str):
                data[key] = str(data[key])

        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.post(self._url(path), data=data) as response:
                        return await self._parse(response)
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

    async def post_json(self, path: str, data: dict[str, Any], no_check_mimetype: bool = False) -> dict | list:
        for key in data:
            if not isinstance(data[key], str):
                data[key] = str(data[key])

        async with self._limiter:
            for i in range(1, 4):
                try:
                    async with self._session.post(self._url(path), data=data) as response:
                        if not no_check_mimetype:
                            return await response.json()
                        else:
                            return await response.json(content_type=None)
                except client_exceptions.ServerDisconnectedError as e:
                    if i >= 3:
                        raise e
                    else:
                        logging.debug(f'ServerDisconnectedError occurred (retry {i}/2 in 5 seconds)')
                        await asyncio.sleep(5)
            else:
                raise AssertionError

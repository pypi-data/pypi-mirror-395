from os import PathLike
from typing import Union

"""
import aiofiles
from aiofiles.threadpool.binary import AsyncBufferedIOBase
"""

from .. import Moodle


class SubmissionFile:
    def __init__(self, md: Moodle, name: str, url: str):
        self._md: Moodle = md
        self._name: str = name
        self._url: str = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    def __str__(self):
        return self.name

    async def fetch(self) -> bytes:
        return await self._md.session.get_bytes(self._url)

    # TODO dump submission
    """
    async def dump(self, file: Union[str, bytes, PathLike, AsyncBufferedIOBase]):
        content = await self.fetch()

        if isinstance(file, AsyncBufferedIOBase):
            await file.write(content)
        else:
            async with aiofiles.open(file, 'wb') as fp:
                await fp.write(content)
    """

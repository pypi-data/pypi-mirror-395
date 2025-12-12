from typing import Tuple

from .Spawner import Spawner
from ..Stage import Stage


class DockerSpawner(Spawner):
    def __init__(self, image: str, server_name: str = None):
        super().__init__(server_name)
        self.image: str = image

    def url(self, successors: Tuple[Stage, ...]) -> str:
        return self._get(successors, image=self.image)

from typing import Dict, Tuple

from ..Stage import Stage


class Application(Stage):
    def __init__(self, path: str, **kwargs):
        super().__init__()

        self.path: str = path
        self.kwargs: Dict = kwargs

    def url(self, successors: Tuple[Stage, ...]) -> str:
        path = f'{self.path}'

        if self.kwargs:
            params = '&'.join(f'{key}={self.encode(value)}' for key, value in self.kwargs.items())
            path += f'?{params}'

        return path

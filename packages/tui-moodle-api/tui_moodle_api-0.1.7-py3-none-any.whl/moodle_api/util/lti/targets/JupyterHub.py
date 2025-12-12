from typing import Tuple

from ..Stage import Stage


class JupyterHub(Stage):
    def __init__(self, name: str):
        super().__init__()
        self.name: str = name

    def url(self, successors: Tuple[Stage, ...]) -> str:
        url = f'https://{self.name}/'

        if len(successors) > 0:
            url += f'?next={successors[0].encoded_url(successors[1:])}'

        return url

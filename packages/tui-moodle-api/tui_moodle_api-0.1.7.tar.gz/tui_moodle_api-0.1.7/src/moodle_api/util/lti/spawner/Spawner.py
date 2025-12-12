from typing import Optional, Tuple

from ..Stage import Stage


class Spawner(Stage):
    def __init__(self, server_name: str = None):
        super().__init__()
        self.server_name: Optional[str] = server_name

    def _get(self, successors: Tuple[Stage, ...], **kwargs) -> str:
        params = {
            **{
                k: self.encode(v)
                for k, v in kwargs.items()
            }
        }

        if self.server_name is not None:
            params['server_name'] = self.encode(self.server_name),

            if len(successors) > 0:
                params['next'] = self.encode(
                    f'/hub/user-redirect/{self.server_name}/{successors[0].url(successors[1:])}')

        else:
            if len(successors) > 0:
                params['next'] = self.encode(f'/hub/user-redirect/{successors[0].url(successors[1:])}')

        query = '&'.join(f'{k}={v}' for k, v in params.items())
        return f'/hub/spawn?{query}'

    def url(self, successors: Tuple[Stage, ...]) -> str:
        return self._get(successors)

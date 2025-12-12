import urllib.parse
from typing import Optional, Tuple


class Stage:
    def __init__(self):
        self.parent: Optional[Stage] = None

    @staticmethod
    def encode(value: str) -> str:
        return urllib.parse.quote(value, safe='')

    def encoded_url(self, successors: Tuple['Stage', ...]) -> str:
        return self.encode(self.url(successors))

    def url(self, successors: Tuple['Stage', ...]) -> str:
        raise NotImplementedError

    def __str__(self, successors: Tuple['Stage', ...] = ()) -> str:
        if self.parent is not None:
            return self.parent.__str__((self,) + successors)
        else:
            return self.url(successors)

    def __add__(self, other: 'Stage') -> 'Stage':
        other.parent = self
        return other

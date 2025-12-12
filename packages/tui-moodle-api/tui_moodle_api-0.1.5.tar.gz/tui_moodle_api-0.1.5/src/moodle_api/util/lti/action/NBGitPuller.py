from typing import Tuple

from ..Stage import Stage


class NBGitPuller(Stage):
    def __init__(self, repo: str, branch: str, target_path: str):
        super().__init__()
        self.repo: str = repo
        self.branch: str = branch
        self.target_path: str = target_path

    def url(self, successors: Tuple[Stage, ...]) -> str:
        repo = self.encode(self.repo)
        branch = self.encode(self.branch)
        target_path = self.encode(self.target_path)

        path = f'git-pull?repo={repo}&branch={branch}&targetPath={target_path}'

        if len(successors) > 0:
            path += f'&urlpath={successors[0].encoded_url(successors[1:])}'

        return path

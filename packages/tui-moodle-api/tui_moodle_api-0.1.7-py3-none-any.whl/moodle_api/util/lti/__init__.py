from .Stage import Stage
from .action import *
from .application import *
from .spawner import *
from .targets import *


def generate(hub: str, image: str, git_repo: str, git_branch: str, git_target: str, start: str) -> str:
    hub = JupyterHub(hub)
    image = hub + DockerSpawner(image)
    git = image + NBGitPuller(git_repo, git_branch, git_target)
    lab = git + JupyterLab(f'{git_target}/{start}')

    return str(lab)

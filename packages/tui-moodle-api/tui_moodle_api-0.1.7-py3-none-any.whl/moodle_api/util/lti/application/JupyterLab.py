from .Application import Application


class JupyterLab(Application):
    def __init__(self, path: str = ''):
        super().__init__(f'lab/tree/{path}')

from .Application import Application


class NBClassic(Application):
    def __init__(self, path: str = ''):
        super().__init__(f'nbclassic/notebooks/{path}')

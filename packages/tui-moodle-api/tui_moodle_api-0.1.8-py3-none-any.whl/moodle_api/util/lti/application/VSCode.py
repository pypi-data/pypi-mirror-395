from .Application import Application


class VSCode(Application):
    def __init__(self, folder: str = None):
        if folder is not None:
            super().__init__('vscode', folder=folder)
        else:
            super().__init__('vscode')

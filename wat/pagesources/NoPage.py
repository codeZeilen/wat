from .AbstractPage import AbstractPage
import pathlib

class NoPage(AbstractPage):

    def __init__(self, name: str = ""):
        self.name = name

    def description(self) -> str:
        absolute_path = pathlib.Path(self.name).absolute()
        if not absolute_path.exists():
            return "no description found, consider filing an issue at https://github.com/codeZeilen/wat"
        else:
            return "no description found, consider adding a page at https://github.com/codeZeilen/wat-pages"
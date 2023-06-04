from .AbstractPage import AbstractPage


class NoPage(AbstractPage):

    def __init__(self, name: str = ""):
        self.name = name

    def description(self) -> str:
        return "no description found"

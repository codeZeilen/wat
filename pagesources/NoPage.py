from AbstractPage import AbstractPage

class NoPage(AbstractPage):

    def description(self) -> str:
        return "no description found"
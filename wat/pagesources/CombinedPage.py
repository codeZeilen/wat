from abc import abstractmethod
from . import AbstractPage


class CombinedPage(AbstractPage):

    def __init__(self, pages) -> None:
        self.pages = pages

    @classmethod
    def get_page(cls, name: str):
        return False

    def description(self) -> str:
        description = ""
        for page in self.pages:
            description += "\n - ({}) {}".format(page.page_type(), page.description())
        return description

    @abstractmethod
    def page_type(self) -> str:
        return "list"

    def page_name(self) -> str:
        return self.pages[0].page_name()

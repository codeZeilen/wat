from abc import abstractmethod
from . import AbstractPage


class CombinedPage(AbstractPage):

    def __init__(self, type_page, description_page) -> None:
        self.type_page: AbstractPage = type_page
        self.description_page: AbstractPage = description_page

    @classmethod
    def has_page(cls, name: str) -> bool:
        return False

    @classmethod
    def get_page(cls, name: str):
        return False

    def description(self) -> str:
        return self.description_page.description()

    @abstractmethod
    def page_type(self) -> str:
        return self.type_page.page_type()

    def page_name(self) -> str:
        return self.type_page.page_name()

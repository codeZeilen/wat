from abc import abstractmethod
from . import AbstractPage
import itertools


class CombinedPage(AbstractPage):

    def __init__(self, pages) -> None:
        self.pages = pages

    @classmethod
    def get_page(cls, name: str):
        return False

    def all_pages_have_same_type(cls):
        return all(page.page_type() == cls.pages[0].page_type() for page in cls.pages)

    def description(self) -> str:
        if self.all_pages_have_same_type():
            return self.single_description()
        else:
            return self.list_description()
            
    def single_description(self) -> str:
        return self.pages[-1].description()

    def list_description(self) -> str:
        description = ""
        page_groups = itertools.groupby(self.pages, lambda page: page.page_type())
        for page_type, page_group in page_groups:
            page = list(page_group)[-1]
            description += "\n - ({}) {}".format(page_type, page.description())
        return description

    @abstractmethod
    def page_type(self) -> str:
        if self.all_pages_have_same_type():
            return self.pages[0].page_type()
        else:
            return "list"

    def page_name(self) -> str:
        return self.pages[0].page_name()

from abc import abstractmethod


class AbstractPage(object):

    def __init__(self) -> None:
        self.name: str = ""

    @classmethod
    @abstractmethod
    def has_page(cls, name: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def get_page(cls, name: str):
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def page_type(self) -> str:
        pass

    @abstractmethod
    def page_name(self) -> str:
        return self.name

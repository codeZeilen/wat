from abc import abstractmethod


class AbstractPage(object):

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
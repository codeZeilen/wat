from abc import abstractmethod


class AbstractPage(object):

    def __init__(self) -> None:
        self.name: str = ""

    @classmethod
    @abstractmethod
    def get_page(cls, name: str):
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def update_page_source(cls):
        pass

    @classmethod
    def raiseKeyError(cls, name: str):
        raise KeyError("No page found for name: {}".format(name))

    @abstractmethod
    def page_type(self) -> str:
        return ""

    def page_name(self) -> str:
        return self.name

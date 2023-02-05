from typing import Dict
from .AbstractPage import AbstractPage
import json
import os


class FSPathPage(AbstractPage):

    pages = {}

    def __init__(self, path):
        self.path = path

    @classmethod
    def is_path(cls, path):
        return os.path.exists(path)

    @classmethod
    def has_page(cls, path) -> bool:
        return cls.is_path(path) and path in cls.all_pages()

    @classmethod
    def get_page(cls, path) -> 'FSPathPage':
        return cls(path)

    @classmethod
    def all_pages(cls) -> Dict[str, str]:
        if not cls.pages:
            with open("./fspages.json") as pages_file:
                cls.pages = json.load(pages_file)
        return cls.pages

    def description(self, detailed=False) -> str:
        return FSPathPage.all_pages().get(self.path, "no page found")

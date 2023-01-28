from typing import List, Dict
from .AbstractPage import AbstractPage
import json
import os


class FSPathPage(AbstractPage):

    with open("./fspages.json") as pages_file:
        pages: Dict[str, str] = json.load(pages_file)

    def __init__(self, path):
        self.path = path

    @classmethod
    def is_path(cls, path):
        return os.path.exists(path)

    @classmethod
    def has_page(cls, path) -> bool:
        return cls.is_path(path) and path in cls.pages

    @classmethod
    def get_page(cls, path) -> 'FSPathPage':
        return cls(path)

    def description(self, detailed=False) -> str:
        return FSPathPage.all_pages().get(self.path, "no page found")

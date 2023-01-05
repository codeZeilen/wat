from typing import List, Optional, Tuple, Union, Type
from .AbstractPage import AbstractPage
import json, os

class FSPathPage(AbstractPage):

    pages = None
    with open("./fspages.json") as pages_file:
        pages = json.load(pages_file)

    def __init__(self, path):
        self.path = path

    @classmethod
    def is_path(cls, path):
        return os.path.exists(path)

    @classmethod
    def get_page(cls, path) -> Type['FSPathPage']:
        return cls(path)

    def description(self, detailed = False) -> str:
        return FSPathPage.pages.get(self.path, "no page found")
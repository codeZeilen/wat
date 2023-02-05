from typing import Dict
from .AbstractPage import AbstractPage
import json
import os
import pathlib


class FSPathPage(AbstractPage):

    pages = {}
    pages_file_path = pathlib.Path(__file__).parent / ".." / ".." / "fspages.json"

    def __init__(self, path):
        self.path = pathlib.Path(self.path).absolute()

    @classmethod
    def is_path(cls, path):
        return os.path.exists(path)

    @classmethod
    def has_page(cls, path) -> bool:
        absolute_path = pathlib.Path(path).absolute().as_posix()
        return cls.is_path(absolute_path) and absolute_path in cls.all_pages()

    @classmethod
    def get_page(cls, path) -> 'FSPathPage':
        return cls(path)

    @classmethod
    def all_pages(cls) -> Dict[str, str]:
        if not cls.pages:
            with open(cls.pages_file_path) as pages_file:
                cls.pages = json.load(pages_file)
        return cls.pages

    def description(self, detailed=False) -> str:
        return FSPathPage.all_pages().get(self.path.as_posix(),
            "no page found")

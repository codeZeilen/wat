from typing import Dict
from .AbstractPage import AbstractPage
import json
import pathlib
import pkgutil


class FSPathPage(AbstractPage):

    pages = {}
    pages_file_path = "fspages.json"

    def __init__(self, path_object: pathlib.Path, page_content: str = ""):
        self.path = path_object
        self.page_content = page_content

    @classmethod
    def content_from_pattern(cls, path) -> str:
        for pattern in cls.all_pages()["patterns"]:
            if path.match(pattern):
                return cls.all_pages()["patterns"][pattern]
        return ""

    @classmethod
    def get_page(cls, path) -> 'FSPathPage':
        absolute_path = pathlib.Path(path).absolute()
        page_content = None
        if absolute_path.exists():
            page_content = cls.all_pages()["absolute_paths"].get(absolute_path.as_posix(), None)
            if page_content:
                return cls(absolute_path, page_content)
            
            page_content = cls.all_pages()["individual_files"].get(absolute_path.name, None)
            if page_content:
                return cls(absolute_path, page_content)

            page_content = cls.content_from_pattern(absolute_path)
            if page_content:
                return cls(absolute_path, page_content)
        cls.raiseKeyError(path)

    @classmethod
    def initialize_pages(cls) -> None:
        cls.pages = json.loads(pkgutil.get_data(__name__, cls.pages_file_path))

    @classmethod
    def all_pages(cls) -> Dict[str, Dict[str, str]]:
        if not cls.pages:
            cls.initialize_pages()
        return cls.pages

    def description(self, detailed=False) -> str:
        return self.page_content

    def page_type(self) -> str:
        return "directory" if self.path.is_dir() else "file"

    def page_name(self) -> str:
        return self.path.as_posix()

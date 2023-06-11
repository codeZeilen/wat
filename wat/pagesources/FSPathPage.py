from typing import Optional
from .AbstractPage import AbstractPage
import os
import pathlib
from . import FileCache
from .GlobTrie import GlobTrie 

DOWNLOAD_CACHE_URL = os.environ.get(
    'WAT_FSPATH_PAGES_DOWNLOAD_CACHE_URL',
    'http://github.com/codeZeilen/wat-pages/releases/latest/download/fs-path-pages.zip'
)
FSPATH_PAGES_CACHE = FileCache.FileCache('fs_pages', DOWNLOAD_CACHE_URL)


class FSPathPage(AbstractPage):

    pages: Optional['GlobTrie'] = None

    def __init__(self, path_object: pathlib.Path, page_content: str = ""):
        self.path = path_object
        self.page_content = page_content

    @classmethod
    def get_page(cls, path: str) -> 'FSPathPage':
        absolute_path = pathlib.Path(path).absolute()
        if not absolute_path.exists():
            cls.raiseKeyError(path)
       
        page_file_name = cls.try_absolute_path(absolute_path)

        if not page_file_name:  # Try individual files
            page_file_name = cls.try_individual_files(absolute_path)

        if not page_file_name:
            cls.raiseKeyError(path)

        page_content = cls.get_page_content(page_file_name)

        return cls(absolute_path, page_content)

    @classmethod
    def get_page_content(cls, page_file_name):
        with FSPATH_PAGES_CACHE.page_file(page_file_name) as f:
            page_content = f.read()
        return page_content.split("---")[-1].strip()

    @classmethod
    def try_absolute_path(cls, absolute_path) -> Optional[str]:
        try:
            return cls.all_pages().get(absolute_path.as_posix())
        except KeyError:
            return None

    @classmethod
    def try_individual_files(cls, absolute_path) -> Optional[str]:
        try:
            return cls.all_pages().get(absolute_path.name)
        except KeyError:
            return None

    @classmethod
    def initialize_pages(cls) -> None:
        with FSPATH_PAGES_CACHE.index_file() as f:
            cls.pages = GlobTrie.load(f)

    @classmethod
    def reset_pages(cls) -> None:
        cls.pages = None

    @classmethod
    def all_pages(cls) -> 'GlobTrie':
        if not cls.pages:
            cls.initialize_pages()
        return cls.pages

    def description(self, detailed=False) -> str:
        return self.page_content

    def page_type(self) -> str:
        return "directory" if self.path.is_dir() else "file"

    def page_name(self) -> str:
        return self.path.as_posix()

    @classmethod
    def update_page_source(cls) -> None:
        FSPATH_PAGES_CACHE.update_cache()
        print("Updated pages for files and folders.")

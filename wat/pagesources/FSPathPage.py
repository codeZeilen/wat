from typing import Dict, Optional
from .AbstractPage import AbstractPage
import json
import pathlib
import fnmatch
from . import FileCache


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
        with FileCache.page_file('fs_pages', page_file_name) as f:
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
        relative_path = '**/' + absolute_path.name
        try:
            return cls.all_pages().get(relative_path)
        except KeyError:
            return None

    @classmethod
    def initialize_pages(cls) -> None:
        with FileCache.index_file('fs_pages') as f:
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


class GlobTrie(object):

    @classmethod
    def load(cls, glob_trie_file) -> 'GlobTrie':
        new_trie = cls()
        new_trie.trie = json.load(glob_trie_file)
        return new_trie

    def __init__(self):
        self.trie: Dict = dict()

    def store(self, glob_trie_file_path) -> None:
        with open(glob_trie_file_path, 'w') as f:
            json.dump(self.trie, f)

    def store_string(self) -> str:
        return json.dumps(self.trie)

    def add(self, glob_pattern, page_file_name: str) -> None:
        current_node = self.trie
        for part in pathlib.Path(glob_pattern).parts:
            if part == "**":
                raise ValueError("Glob pattern cannot contain '**'")
            if "*" in part:
                if "globs" not in current_node:
                    current_node["globs"] = {}
                
                if part in current_node["globs"]:
                    current_node = current_node["globs"][part]
                else:
                    current_node["globs"][part] = {}
                    current_node = current_node["globs"][part]
            else:
                if part in current_node:
                    current_node = current_node[part]
                else:
                    current_node[part] = {}
                    current_node = current_node[part]
        current_node["value"] = page_file_name

    def get(self, path) -> str:
        current_node = self.trie
        for part in pathlib.PosixPath(path).parts:
            if part in current_node:
                current_node = current_node[part]
            elif "globs" in current_node:
                for pattern in current_node["globs"]:
                    if fnmatch.fnmatch(part, pattern):
                        current_node = current_node["globs"][pattern]
                        break  # We assume that there is only one match and break the globs loop
            else:
                raise KeyError(path)
        return current_node['value']

import json
import pathlib
import fnmatch
from typing import Dict


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

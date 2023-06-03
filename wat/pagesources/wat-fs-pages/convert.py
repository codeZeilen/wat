import json
import pathlib
import fnmatch
from typing import Dict


class GlobTree(object):

    def __init__(self, glob_tree):
        self.tree: Dict = glob_tree

    def store(self, glob_tree_file_path) -> None:
        with open(glob_tree_file_path, 'w') as f:
            json.dump(self.tree, f)

    def add(self, glob_pattern, page_file_name: str) -> None:
        current_node = self.tree
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
        current_node = self.tree
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

new_index = GlobTree(dict())

data = json.loads(open("./index.json").read())

for group_key in ("absolute_paths", "individual_files", "patterns"):
    group = data[group_key]
    for key in group:
        if key.startswith("__"):
            continue
        file_name = key if key[0] != "/" else key[1:]
        file_name = file_name.replace("/", "-")
        file_name = file_name.replace("*", "glob")
        file_name = file_name + ".md"
        new_index.add(key, file_name)
        
        file_content = "---\n"
        if "__license" in group and group["__license"] != "":
            file_content += "license: " + group["__license"] 
            file_content += "\n"
        file_content += "path: " + key + "\n"
        
        file_content += "---\n\n"
        file_content += group[key]

        with open(file_name, "w") as f:
            f.write(file_content)

new_index.store("new_index.json")

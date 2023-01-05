#!/usr/bin/env python3

from typing import List, Optional, Tuple, Union, Type

import tldr
from argparse import ArgumentParser
import os
import json
import subprocess

class WhatIsHelpPage(object):
    """`whatis` makes use of the man page infrastructure of the OS.
    This also covers the output of `apropos`, `info`, and `man`."""

    def __init__(self, name, content: str):
        self.page_name = name
        self.content = content

    def description(self, detailed = False) -> str:
        return self.content

    @staticmethod
    def run_whatis(name: str):
        return subprocess.run(["whatis", name], capture_output=True)

    @staticmethod
    def has_page(name: str) -> bool:
        process = WhatIsHelpPage.run_whatis(name)
        return process.returncode == 0

    @staticmethod
    def get_page(name: str) -> 'WhatIsHelpPage':
        process = WhatIsHelpPage.run_whatis(name)
        description = process.stdout.decode('utf-8')
        description = description.split(" - ")[1].strip()
        return WhatIsHelpPage(name, description)

class OSHelpPage(object):
    """`help` documents the built-in commands of bash"""

    def __init__(self, name, content: str):
        self.page_name = name
        self.content = content

    def description(self, detailed = False) -> str:
        return self.content

    @staticmethod
    def run_help(name: str):
        return subprocess.run(["/bin/bash", "-c", '"help -d {name}"'.format(name=name)], capture_output=True)
        
    @staticmethod
    def has_page(name: str) -> bool:
        process = OSHelpPage.run_help(name)
        return process.returncode == 0

    @staticmethod
    def get_page(name: str) -> 'OSHelpPage':
        process = OSHelpPage.run_help(name)
        return OSHelpPage(name, str(process.stdout))

class TLDRPage(object):

    def __init__(self, name, content: List[str]):
        self.page_name = name
        self.content = content

    @staticmethod
    def get_page(name: str) -> 'TLDRPage':
        return TLDRPage(name, tldr.get_page(name))

    @staticmethod
    def has_page(name: str) -> bool:
        return tldr.get_page(name) is not False

    def description(self, detailed = False) -> str:
        description = ""
        lines = self.content[2:4] if detailed else self.content[2:3]
        for line in lines:
            line = line.rstrip().decode('utf-8')
            if line[0] == ">":
                line = line[1:].lstrip()
            description = description + line + "\n" 
        return description.rstrip()

class FileOrFolderPage(object):

    pages = None
    with open("./fspages.json") as pages_file:
        pages = json.load(pages_file)

    def __init__(self, path):
        self.path = path

    @staticmethod
    def is_path(path):
        return os.path.exists(path)

    @staticmethod
    def get_page(path) -> Type['FileOrFolderPage']:
        return FileOrFolderPage(path)

    def description(self, detailed = False) -> str:
        return FileOrFolderPage.pages.get(self.path, "no page found")

def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="wat")
    parser.add_argument(
        'name_of_this', type=str, nargs='*', help="name of the thing to lookup", metavar='nameOfThis'
    )
    return parser

def parse_arguments() -> List[str]:
    parser = create_parser()
    arguments = parser.parse_args()
    if not arguments.name_of_this:
        parser.print_help() 
    return arguments.name_of_this

def lookup_page(name: str) -> str:
    if FileOrFolderPage.is_path(name):
        return FileOrFolderPage.get_page(name)
    elif WhatIsHelpPage.has_page(name):
        return WhatIsHelpPage.get_page(name)
    elif OSHelpPage.has_page(name):
        return OSHelpPage.get_page(name)
    elif TLDRPage.has_page(name):
        return TLDRPage.get_page(name)
    else:
        return "no description found"

def print_description(description: str) -> None:
    print(description)

def answer_wat():
    requested_names = parse_arguments()
    for name in requested_names:
        page = lookup_page(name)
        print_description(name + ": " + page.description())

if __name__ == "__main__":
    answer_wat()
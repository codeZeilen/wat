#!/usr/bin/env python3

from typing import List, Optional, Tuple, Union, Type

import tldr
from argparse import ArgumentParser

class TLDRPage(object):

    def __init__(self, name, content: List[str]):
        self.page_name = name
        self.content = content

    @staticmethod
    def get_page(name: str) -> Type['TLDRPage']:
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

def lookup_description(name: str) -> str:
    if TLDRPage.has_page(name):
        return TLDRPage.get_page(name).description()
    else:
        return "no description found"

def print_description(description: str) -> None:
    print(description)

def answer_wat():
    requested_names = parse_arguments() 
    for name in requested_names:
        description = lookup_description(name)
        print_description(name + ": " + description)

if __name__ == "__main__":
    answer_wat()
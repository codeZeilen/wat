#!/usr/bin/env python3

from typing import List, Optional, Tuple, Union, Type

from argparse import ArgumentParser

from pagesources import BashHelpPage, FSPathPage, TLDRPage, WhatIsPage

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
    if FSPathPage.is_path(name):
        return FSPathPage.get_page(name)
    elif WhatIsPage.has_page(name):
        return WhatIsPage.get_page(name)
    elif BashHelpPage.has_page(name):
        return BashHelpPage.get_page(name)
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
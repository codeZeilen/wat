#!/usr/bin/env python3

from typing import List

from argparse import ArgumentParser

from .pagesources import NoPage, AbstractPage, BashHelpPage, FSPathPage, \
    WhatIsPage, TLDRPage, SystemCtlPage
from . import __version__


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="wat")
 
    parser.add_argument(
        'name_of_this', type=str, nargs='*', 
        help="name of the thing to lookup", metavar='nameOfThis'
    )
    parser.add_argument('--version', action='version', version=__version__)

    return parser


def parse_arguments() -> List[str]:
    parser = create_parser()
    arguments = parser.parse_args()
    if not arguments.name_of_this:
        parser.print_help()
    return arguments.name_of_this


def lookup_page(name: str) -> 'AbstractPage':
    if FSPathPage.has_page(name):
        return FSPathPage.get_page(name)
    elif BashHelpPage.has_page(name):
        return BashHelpPage.get_page(name)
    elif SystemCtlPage.has_page(name):
        return SystemCtlPage.get_page(name)
    elif TLDRPage.has_page(name):
        return TLDRPage.get_page(name)
    elif WhatIsPage.has_page(name):
        return WhatIsPage.get_page(name)
    else:
        return NoPage()


def print_description(page: AbstractPage) -> None:
    print("{0} ({1}): {2}".format(page.page_name(), page.page_type(), page.description()))


def answer_wat():
    requested_names = parse_arguments()
    for name in requested_names:
        page = lookup_page(name)
        print_description(page)

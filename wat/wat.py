#!/usr/bin/env python3

from typing import List

from argparse import ArgumentParser

from wat.pagesources import CombinedPage

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
    result_pages = []
    # The following ordering constitutes a priotization of 
    # the different page sources
    if FSPathPage.has_page(name):
        result_pages.append(FSPathPage.get_page(name))
    if BashHelpPage.has_page(name):
        result_pages.append(BashHelpPage.get_page(name))
    if SystemCtlPage.has_page(name):
        result_pages.append(SystemCtlPage.get_page(name))
    if WhatIsPage.has_page(name):
        result_pages.append(WhatIsPage.get_page(name))
    if TLDRPage.has_page(name):
        result_pages.append(TLDRPage.get_page(name))
    
    result_page = NoPage()
    if len(result_pages) > 1:
        # We use the most specific type with the most extensive description
        if result_pages[0].page_type() == result_pages[-1].page_type():
            result_page = result_pages[-1]
        else:
            result_page = CombinedPage(result_pages[0], result_pages[-1])
    elif (len(result_pages) == 1):
        result_page = result_pages[0]
    
    return result_page


def print_description(page: AbstractPage) -> None:
    print("{0} ({1}): {2}".format(page.page_name(), page.page_type(), page.description()))


def answer_wat():
    requested_names = parse_arguments()
    for name in requested_names:
        page = lookup_page(name)
        print_description(page)

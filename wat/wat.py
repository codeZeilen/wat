#!/usr/bin/env python3

from typing import List

from argparse import ArgumentParser, Namespace

from wat.pagesources import CombinedPage

from .pagesources import NoPage, AbstractPage, BashHelpPage, FSPathPage, \
    WhatIsPage, TLDRPage, SystemCtlPage, PackageManagerPage
from . import __version__


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="wat")
 
    parser.add_argument(
        'name_of_this', type=str, nargs='*', 
        help="name of the thing to lookup", metavar='nameOfThis'
    )
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--update', '-u', action='store_true')
    parser.add_argument('--ignore-empty-result', action='store_true')
    return parser


def parse_arguments() -> 'Namespace':
    parser = create_parser()
    arguments = parser.parse_args()
    if not arguments.name_of_this and not arguments.update:
        parser.print_help()
    return arguments


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
    if PackageManagerPage.has_page(name):
        result_pages.append(PackageManagerPage.get_page(name))
    
    result_page = NoPage(name)
    if len(result_pages) > 1:
        # We use the most specific type with the most extensive description
        if result_pages[0].page_type() == result_pages[-1].page_type():
            result_page = result_pages[-1]
        else:
            result_page = CombinedPage(result_pages[0], result_pages[-1])
    elif (len(result_pages) == 1):
        result_page = result_pages[0]
    
    return result_page


def print_description(page: AbstractPage, ignore_empty_page: bool=False) -> None:
    page_type = page.page_type()
    if page_type:
        print("{0} ({1}): {2}".format(page.page_name(), page_type, page.description()))
    elif not ignore_empty_page:
        print("{0}: {1}".format(page.page_name(), page.description()))


def update_page_sources() -> None:
    for page_source in [FSPathPage, BashHelpPage, SystemCtlPage, WhatIsPage, TLDRPage, PackageManagerPage]:
        page_source.update_page_source()


def answer_wat():
    arguments = parse_arguments()
    if arguments.update:
        update_page_sources()
        raise SystemExit(0)
    for name in arguments.name_of_this:
        page = lookup_page(name)
        print_description(page, arguments.ignore_empty_result)

#!/usr/bin/env python3

from typing import List

from argparse import ArgumentParser, Namespace

from wat.pagesources import CombinedPage, NoPage, AbstractPage, BashHelpPage, FSPathPage, WhatIsPage, TLDRPage, SystemCtlPage, PackageManagerPage

from . import __version__

# The following ordering constitutes a priotization of pages sources
# from general to specific.
PAGE_SOURCES = [FSPathPage, BashHelpPage, SystemCtlPage, WhatIsPage, TLDRPage, PackageManagerPage]


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="wat")
 
    parser.add_argument(
        'name_of_this', type=str, nargs='*', 
        help="name of the thing to lookup", metavar='name'
    )
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--update', '-u', action='store_true', help="update the page sources")
    parser.add_argument('--skip-empty-result', action='store_true', help="if there is no result, don't print anything")
    return parser


def parse_arguments() -> 'Namespace':
    parser = create_parser()
    arguments = parser.parse_args()
    if not arguments.name_of_this and not arguments.update:
        parser.print_help()
    return arguments


def lookup_page(name: str) -> 'AbstractPage':
    result_pages = []
    for page_source in PAGE_SOURCES:
        try:
            result_pages.append(page_source.get_page(name))
        except KeyError:
            pass

    result_page = NoPage(name)
    if len(result_pages) > 1:
        result_page = CombinedPage(result_pages)
    elif (len(result_pages) == 1):
        result_page = result_pages[0]
    
    return result_page


def print_description(page: AbstractPage, skip_empty_result: bool=False) -> None:
    page_type = page.page_type()
    if page_type:
        print("{0} ({1}): {2}".format(page.page_name(), page_type, page.description()))
    elif not skip_empty_result:
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
        print_description(page, arguments.skip_empty_result)

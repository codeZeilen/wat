import os
import pathlib
import sys


def index_file(page_collection_name):
    index_path = cache_dir_path() / page_collection_name / 'index.json'
    return open(index_path, 'r')


def page_file(page_collection_name, file_name):
    file_path = cache_dir_path() / page_collection_name / file_name
    return open(file_path, 'r')


# The symbols adhere to the tldr naming scheme
def os_symbol() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('win32'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'osx'
    else:
        return 'common'


def cache_dir_path() -> 'pathlib.Path':
    base_directory: str = ''
    if os.environ.get('XDG_CACHE_HOME', False):
        base_directory = os.environ.get('XDG_CACHE_HOME')
    elif os.environ.get('HOME', False):
        base_directory = os.environ.get('HOME')
    else:
        base_directory = os.path.expanduser("~")

    return pathlib.Path(base_directory) / '.cache' / 'wat'

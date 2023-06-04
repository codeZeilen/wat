from io import BytesIO
import os
import pathlib
import sys
from zipfile import ZipFile
from urllib.request import urlopen, Request

REQUEST_HEADERS = {'User-Agent': 'wat-python-client'}


class FileCache(object):

    def __init__(self, collection_name, archive_location) -> None:
        self.collection_name: str = collection_name
        self.archive_location: str = archive_location

    def index_file(self):
        self.ensure_cache_dir_exists()
        index_path = self.base_dir_path() / 'index.json'
        return open(index_path, 'r')

    def page_file(self, file_name):
        self.ensure_cache_dir_exists()
        file_path = self.base_dir_path() / file_name
        return open(file_path, 'r')

    def ensure_cache_dir_exists(self):
        if not self.base_dir_path().exists():
            self.base_dir_path().mkdir(parents=True)
            self.update_cache()

    def update_cache(self):
        req = urlopen(Request(
            self.archive_location,
            headers=REQUEST_HEADERS
        ))
        zipfile = ZipFile(BytesIO(req.read()))
        zipfile.extractall(path=str(self.base_dir_path()))

    def base_dir_path(self) -> 'pathlib.Path':
        return self.cache_dir_path() / self.collection_name

    # The symbols adhere to the tldr naming scheme
    def os_symbol(self) -> str:
        if sys.platform.startswith('linux'):
            return 'linux'
        elif sys.platform.startswith('win32'):
            return 'windows'
        elif sys.platform.startswith('darwin'):
            return 'osx'
        else:
            return 'common'

    def cache_dir_path(self) -> 'pathlib.Path':
        base_directory: str = ''
        if os.environ.get('XDG_CACHE_HOME', False):
            base_directory = os.environ.get('XDG_CACHE_HOME')
        elif os.environ.get('HOME', False):
            base_directory = os.environ.get('HOME')
        else:
            base_directory = os.path.expanduser("~")

        return pathlib.Path(base_directory) / '.cache' / 'wat'

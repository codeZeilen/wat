import os
import pathlib

from pyfakefs.fake_filesystem_unittest import Patcher
from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch

from wat.pagesources import FSPathPage
from wat.pagesources import GlobTrie
from wat.pagesources import FileCache


class TestFSPathPage(TestCase):

    def setUp(self) -> None:
        super().setUp()
        FileCache.FileCache.cache_dir_path = lambda self: pathlib.Path('/home/someUser/.cache/wat')
        FSPathPage.reset_pages()
        FSPathPage.initialize_pages()

    @classmethod
    def create_cached_fs_page(cls, name, content):
        cls.fake_fs().create_file("/home/someUser/.cache/wat/fs_pages/{}".format(name), 
          contents=content)   

    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        trie = GlobTrie()
        trie.add('/home/*/.bashrc', 'globbashrc.md')
        trie.add('/bin', 'bin.md')
        trie.add('/etc/hosts', 'etc-hosts.md')
        trie.add('/etc', 'etc.md')
        bashrc_description = 'bashrc description'

        cls.fake_fs().create_file("/home/someUser/.bashrc", contents="test")
        cls.fake_fs().create_file("/etc/hosts", contents="test")
        cls.fake_fs().create_dir("/bin")
        cls.create_cached_fs_page("index.json", trie.store_string())
        cls.create_cached_fs_page('globbashrc.md', bashrc_description)
        cls.create_cached_fs_page('bin.md', '---\n---\n\n/bin is a place for most commonly used programs')
        cls.create_cached_fs_page('etc.md', 'test')
        cls.create_cached_fs_page('etc-hosts.md', '/etc/hosts is a file that contains the IP addresses')

    def test_get_page_for_absolute_path_directory(self):
        page = FSPathPage.get_page("/bin")
        self.assertTrue(page.path.as_posix() == "/bin")
        self.assertTrue(page.description().startswith("/bin is a place for most commonly"))

    def test_get_page_for_absolute_path_file(self):
        page = FSPathPage.get_page("/etc/hosts")
        self.assertTrue(page.path.as_posix() == "/etc/hosts")
        self.assertFalse(page.description() == "no page found")

    def test_get_page_for_relative_path_file(self):
        os.chdir('/etc')
        page = FSPathPage.get_page("hosts")
        self.assertTrue(page.path.as_posix() == "/etc/hosts")
        self.assertFalse(page.description() == "no page found")

    def test_get_page_for_relative_path_in_variable_dir(self):
        os.chdir('/home/someUser')
        page = FSPathPage.get_page(".bashrc")
        self.assertTrue(page.path.as_posix() == "/home/someUser/.bashrc")
        self.assertTrue(page.description() == 'bashrc description')

    #
    # Page Type
    #

    def test_page_type_for_file(self):
        os.chdir('/etc')
        self.assertTrue(FSPathPage.get_page("hosts").page_type() == "file")

    def test_page_type_for_directory(self):
        self.assertTrue(FSPathPage.get_page("/etc").page_type() == "directory")

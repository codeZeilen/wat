import os
import pathlib

from pyfakefs.fake_filesystem_unittest import Patcher
import unittest
from unittest.mock import patch

from wat.pagesources import FSPathPage
from wat.pagesources import GlobTrie
from wat.pagesources import FileCache

class TestFSPathPage(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        FSPathPage.reset_pages()

    def test_get_page_for_absolute_path_directory(self):
        page = FSPathPage.get_page("/bin")
        self.assertTrue(page.path.as_posix() == "/bin")
        self.assertTrue("/bin is a place for most commonly" in page.description())

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
        trie = GlobTrie()
        trie.add('/home/*/.bashrc', 'globbashrc.md')
        page_content = 'bashrc description'

        with Patcher() as patcher:
            patcher.fs.create_file("/home/someUser/.bashrc", contents="test")
            patcher.fs.create_file("/home/someUser/.cache/wat/fs_pages/index.json", 
            contents=trie.store_string())
            patcher.fs.create_file("/home/someUser/.cache/wat/fs_pages/globbashrc.md", 
            contents=page_content)

            with patch.object(FileCache, 'cache_dir_path', return_value=pathlib.Path('/home/someUser/.cache/wat')):
                os.chdir('/home/someUser')
                page = FSPathPage.get_page(".bashrc")
                self.assertTrue(page.path.as_posix() == "/home/someUser/.bashrc")
                self.assertTrue(page.description() == page_content)

    #
    # Page Type
    #

    def test_page_type_for_file(self):
        os.chdir('/etc')
        self.assertTrue(FSPathPage.get_page("hosts").page_type() == "file")

    def test_page_type_for_directory(self):
        self.assertTrue(FSPathPage.get_page("/etc").page_type() == "directory")

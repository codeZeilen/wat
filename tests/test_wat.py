from wat import wat
from wat.pagesources import TLDRPage
import mock
import unittest


class WatTest(unittest.TestCase):

    @unittest.skip("Requires installation to work first")
    def test_lookup_name_fs_page(self):
        """
        Does it produce the correct page for a directory by absolute path?
        """
        page = wat.lookup_page("/lib")
        self.assertTrue("/lib contains important dynamic libraries and kernel modules" in page.description())

    @unittest.skip("Requires installation to work first")
    def test_lookup_path_results_in_fs_page(self):
        """
        Does it produce the correct page for a directory by absolute path?
        """
        page = wat.lookup_page("/lib")
        self.assertTrue(type(page).__name__ == "FSPathPage")

    def test_lookup_service_results_in_combined_page(self):
        """
        Many services are documented by tldr, which provides better descriptions.
        """
        page = wat.lookup_page("systemd-sysctl")
        self.assertTrue(type(page).__name__ == "CombinedPage")

    def test_lookup_builtin_results_in_combined_page(self):
        """
        Bash builtins are mostly documented by tldr, which provides better descriptions.
        """
        page = wat.lookup_page("echo")
        self.assertTrue(type(page).__name__ == "CombinedPage")

    def test_lookup_tldr_page(self):
        """
        Does it produce the correct page for a tldr page?
        """
        page = wat.lookup_page("ac")
        self.assertTrue(type(page).__name__ == "TLDRPage")

    def test_lookup_package_manager_page(self):
        """
        Does it produce the correct page for a package?
        """
        page = wat.lookup_page("zeitgeist")
        self.assertTrue(type(page).__name__ == "PackageManagerPage")

    def test_update_page_sources(self):
        """
        Update the page sources.
        """
        with mock.patch.object(TLDRPage, 'update_page_source') as mock_update:
            wat.update_page_sources()
            mock_update.assert_called_once_with()
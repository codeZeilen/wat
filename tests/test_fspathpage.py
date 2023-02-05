import os
from pyfakefs.fake_filesystem_unittest import Patcher

from wat.pagesources import FSPathPage


def test_is_path_for_root_path():
    assert FSPathPage.is_path("/bin/bash")
    assert not FSPathPage.is_path("no_such_path")


def test_is_path_for_local_path():
    os.chdir('/etc')
    assert FSPathPage.is_path("hosts")


def test_has_page_for_root_path():
    assert FSPathPage.has_page("/bin")
    assert not FSPathPage.has_page("no_such_path")


def test_get_page_for_root_path():
    page = FSPathPage.get_page("/bin")
    assert page.path == "/bin"


def test_has_page_for_local_path():
    os.chdir('/etc')
    assert FSPathPage.has_page("hosts")


def test_has_page_for_local_path_in_variable_dir():
    FSPathPage.has_page("/bin")  # To initialize the pages cache
    with Patcher() as patcher:
        patcher.fs.create_file("/home/someUser/.bashrc", contents="test")
        os.chdir('/home/someUser')
        assert FSPathPage.has_page(".bashrc")

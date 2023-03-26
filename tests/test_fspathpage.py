import os
from pyfakefs.fake_filesystem_unittest import Patcher

from wat.pagesources import FSPathPage


#
# Get Page
#

def test_get_page_for_absolute_path_directory():
    page = FSPathPage.get_page("/bin")
    assert page.path.as_posix() == "/bin"
    assert "/bin is a place for most commonly" in page.description()


def test_get_page_for_absolute_path_file():
    page = FSPathPage.get_page("/etc/hosts")
    assert page.path.as_posix() == "/etc/hosts"
    assert not page.description() == "no page found"


def test_get_page_for_relative_path_file():
    os.chdir('/etc')
    page = FSPathPage.get_page("hosts")
    assert page.path.as_posix() == "/etc/hosts"
    assert not page.description() == "no page found"


def test_get_page_for_relative_path_in_variable_dir():
    with Patcher() as patcher:
        patcher.fs.create_file("/home/someUser/.bashrc", contents="test")
        os.chdir('/home/someUser')
        page = FSPathPage.get_page(".bashrc")
        assert page.path.as_posix() == "/home/someUser/.bashrc"
        assert not page.description() == "no page found"


#
# Page Type
#

def test_page_type_for_file():
    os.chdir('/etc')
    assert FSPathPage.get_page("hosts").page_type() == "file"


def test_page_type_for_directory():
    assert FSPathPage.get_page("/etc").page_type() == "directory"

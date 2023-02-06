import os
from wat import wat


def test_lookup_name_fs_page():
    """
    Does it produce the correct page for a directory by absolute path?
    """
    page = wat.lookup_page("/lib")
    assert "/lib contains important dynamic libraries and kernel modules" in page.description()
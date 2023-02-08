import os
from wat import wat


def test_lookup_name_fs_page():
    """
    Does it produce the correct page for a directory by absolute path?
    """
    page = wat.lookup_page("/lib")
    assert "/lib contains important dynamic libraries and kernel modules" in page.description()


def test_lookup_path_results_in_fs_page():
    """
    Does it produce the correct page for a directory by absolute path?
    """
    page = wat.lookup_page("/lib")
    assert type(page).__name__ == "FSPathPage"


def test_lookup_service_results_in_systemctl_page():
    """
    Does it produce the correct page for a service?
    """
    page = wat.lookup_page("systemd-sysctl")
    assert type(page).__name__ == "SystemCtlPage"


def test_lookup_builtin_results_in_bash_page():
    """
    Does it produce the correct page for a bash builtin?
    """
    page = wat.lookup_page("echo")
    assert type(page).__name__ == "BashHelpPage"


def test_lookup_tldr_page():
    """
    Does it produce the correct page for a tldr page?
    """
    page = wat.lookup_page("cut")
    assert type(page).__name__ == "TLDRPage"



"""
Tests for command line interface (CLI)
Based on https://github.com/painless-software/python-cli-test-helpers/tree/main/examples/argparse/tests
"""
from importlib.metadata import version
from os import linesep

from cli_test_helpers import shell


def test_bash_built_in_page():
    """
    Does it produce the correct page for a bash builtin?
    """
    result = shell('wat echo')
    assert 'echo: Print given arguments.' in result.stdout


def test_fs_page():
    """
    Does it produce the correct page for a bash builtin?
    """
    result = shell('wat /lib')
    assert "/lib contains important dynamic libraries and kernel modules" in result.stdout


def test_tldr_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = shell('wat cut')
    assert "Cut out fields from `stdin` or files." in result.stdout


def test_no_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = shell('wat no_such_page')
    assert "no description found" in result.stdout


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = shell('python3 -m wat --help')
    assert result.exit_code == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = shell('wat --help')
    assert result.exit_code == 0


def test_usage():
    """
    Does CLI abort w/o arguments, displaying usage instructions?
    """
    result = shell('wat')

    assert 'usage:' in result.stdout


def test_version():
    """
    Does --version display information as expected?
    """
    expected_version = version('wat')
    result = shell('wat --version')

    assert result.stdout == f"{expected_version}{linesep}"
    assert result.exit_code == 0

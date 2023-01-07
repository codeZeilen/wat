"""
Tests for command line interface (CLI)
Based on https://github.com/painless-software/python-cli-test-helpers/tree/main/examples/argparse/tests
"""
from importlib import import_module
from importlib.metadata import version
from os import linesep
from unittest.mock import patch

import pytest

from cli_test_helpers import ArgvContext, shell


def test_main_module():
    """
    Exercise (most of) the code in the ``__main__`` module.
    """
    import_module('wat.__main__')


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

    assert 'usage:' in result.stderr


def test_version():
    """
    Does --version display information as expected?
    """
    expected_version = version('wat')
    result = shell('wat --version')

    assert result.stdout == f"{expected_version}{linesep}"
    assert result.exit_code == 0


# def test_set_action():
#     """
#     Is action argument available?
#     """
#     with ArgvContext('{{package}}', 'set'):
#         args = {{module}}.cli.parse_arguments()

#     assert args.action == 'set'


# NOTE:
# You can continue here, adding all CLI action and option combinations
# using a non-destructive option, such as --help, to test for the
# availability of the CLI command or option.

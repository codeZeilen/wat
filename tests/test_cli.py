"""
Tests for command line interface (CLI)
Based on https://github.com/painless-software/python-cli-test-helpers/tree/main/examples/argparse/tests
"""
from importlib.metadata import version
from os import linesep
import pytest

from cli_test_helpers import shell, EnvironContext

SYSTEMCTL_AVAILABLE = shell('systemctl').exit_code == 0


def execute_shell_command(command):
    with EnvironContext(LANG='en_EN'):
        return shell(command)


def test_global_config_file_page():
    """
    Does it produce the correct page for a global config file?
    """
    result = execute_shell_command('wat /etc/sudoers')
    assert not result.stderr
    assert result.exit_code == 0
    assert 'The sudoers file contains a list of users' in result.stdout
    assert 'sudoers (file)' in result.stdout


def test_bash_built_in_page():
    """
    Does it produce the correct page for a bash builtin?
    """
    result = execute_shell_command('wat echo')
    assert 'Print given arguments.' in result.stdout
    assert 'echo (builtin)' in result.stdout


def test_fs_page():
    """
    Does it produce the correct page for a bash builtin?
    """
    result = execute_shell_command('wat /lib')
    assert "/lib contains important dynamic libraries and kernel modules" in result.stdout
    assert "/lib (directory)" in result.stdout


@pytest.mark.skipif(not SYSTEMCTL_AVAILABLE, reason="systemctl not available")
def test_systemctl_page_indirect():
    """
    Does it produce the correct page for a service?
    """
    result = execute_shell_command('wat systemd-sysctl')
    assert "Configure kernel parameters at boot" in result.stdout
    assert "systemd-sysctl (service)" in result.stdout


@pytest.mark.skipif(not SYSTEMCTL_AVAILABLE, reason="systemctl not available")
def test_systemctl_page_direct():
    """
    Does it produce the correct page for a service with a direct name?
    """
    result = execute_shell_command('wat systemd-sysctl.service')
    assert "Configure kernel parameters at boot" in result.stdout
    assert "systemd-sysctl (service)" in result.stdout


def test_tldr_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = execute_shell_command('wat cut')
    assert "Cut out fields from `stdin` or files." in result.stdout
    assert "cut (program)" in result.stdout


def test_no_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = execute_shell_command('wat no_such_page')
    assert "no description found" in result.stdout


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = execute_shell_command('python3 -m wat --help')
    assert result.exit_code == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = execute_shell_command('wat --help')
    assert result.exit_code == 0


def test_usage():
    """
    Does CLI abort w/o arguments, displaying usage instructions?
    """
    result = execute_shell_command('wat')

    assert 'usage:' in result.stdout


def test_version():
    """
    Does --version display information as expected?
    """
    expected_version = version('wat')
    result = execute_shell_command('wat --version')

    assert result.stdout == f"{expected_version}{linesep}"
    assert result.exit_code == 0

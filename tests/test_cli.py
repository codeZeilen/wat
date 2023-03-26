"""
Tests for command line interface (CLI)
Based on https://github.com/painless-software/python-cli-test-helpers/tree/main/examples/argparse/tests
"""
from importlib.metadata import version
from os import linesep
import pytest

from cli_test_helpers import shell, EnvironContext

SYSTEMCTL_AVAILABLE = shell('systemctl').exit_code == 0


def setup_module(module):
    "Ensure pages are up to date"
    shell('wat --update')


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
    result = execute_shell_command('wat until')
    assert 'Execute commands as long as a test does not succeed.' in result.stdout
    assert 'until (builtin)' in result.stdout


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
    

@pytest.mark.skipif(not SYSTEMCTL_AVAILABLE, reason="systemctl not available")
def test_systemctl_page_direct():
    """
    Does it produce the correct page for a service with a direct name?
    """
    result = execute_shell_command('wat systemd-sysctl.service')
    assert "Configure kernel parameters at boot" in result.stdout


def test_tldr_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = execute_shell_command('wat ac')
    assert "Print statistics on how long users have been connected." in result.stdout
    assert "ac (program)" in result.stdout


def test_no_page():
    """
    Does it produce the correct page for a tldr page?
    """
    result = execute_shell_command('wat no_such_page')
    assert "no_such_page: no description found" in result.stdout


def test_no_page_ignore_empty():
    """
    Does it produce empty output when no page is found and --ignore-empty-result is set?
    """
    result = execute_shell_command('wat --ignore-empty-result no_such_page')
    assert len(result.stdout) == 0


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


def test_update():
    """
    Does --update at least produce plausible output?
    """
    result = execute_shell_command('wat --update')

    assert 'usage:' not in result.stdout
    assert result.exit_code == 0
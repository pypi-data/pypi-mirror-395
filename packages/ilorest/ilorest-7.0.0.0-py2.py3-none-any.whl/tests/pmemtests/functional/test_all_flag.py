"""Module containing functional tests for the all flag"""
from __future__ import absolute_import

import sys

import pytest

from rdmc_helper import ReturnCodes


@pytest.mark.skip(reason="temporarily remove all flag")
class TestAllFlag(object):
    """Functional Tests for the --all | -a flag"""

    @staticmethod
    def test_all_flag(ilorest, dl360_large):
        """Test for --all flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--all'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_all_flag_with_json(ilorest, dl360_large):
        """Test for --all flag with --json flag specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--all', '--json'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

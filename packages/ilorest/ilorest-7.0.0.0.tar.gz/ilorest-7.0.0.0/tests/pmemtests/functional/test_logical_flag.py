"""Module containing functional tests for the logical flag"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestLogicalFlag(object):
    """Functional Tests for the --logical | -L flag"""

    @staticmethod
    def test_with_no_attributes(ilorest, dl360_large):
        """Test for --logical flag with no attributes specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--logical'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_dimm_flag(ilorest):
        """Test for --logical flag with dimm flag specified"""
        results = ilorest.run(['showdcpmm', '--logical', '--dimm', '1@2'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_json_flag(ilorest, dl360_large):
        """Test for --logical flag with --json flag specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--logical', '--json'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

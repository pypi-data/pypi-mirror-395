"""Module containing functional tests for the 'cleardcpmmpendingconfig' command"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestClearDcpmmPendingConfigCommand(object):
    """Class for functional tests for the cleardcpmmpendingconfig command"""

    @staticmethod
    def test_show_invalid_flag(ilorest):
        """Test function call with invalid flag"""
        results = ilorest.run(['cleardcpmmpendingconfig', '--bad-flag'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_show_help_flag(ilorest):
        """Test function call with help flag"""
        results = ilorest.run(['cleardcpmmpendingconfig', '-h'])
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_without_flag(ilorest, dl360_large):
        """Test for the case when `cleardcpmmpendingconfig` command is run without any flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['cleardcpmmpendingconfig'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_extraneous_attributes(ilorest):
        """
        Test for the case when `cleardcpmmpendingconfig` command is run with extraneous attributes
        """
        results = ilorest.run(['cleardcpmmpendingconfig', 'testargument'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

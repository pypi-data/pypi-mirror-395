"""Module containing functional tests for the showdcpmmpendingconfig command"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestShowDcpmmPendingConfigCommand(object):
    """Class for functional tests for the showdcpmmpendingconfig command"""

    @staticmethod
    def test_show_invalid_flag(ilorest):
        """Test function call with invalid flag"""
        results = ilorest.run(['showdcpmmpendingconfig', '--bad-flag'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_show_help_flag(ilorest):
        """Test function call with help flag"""
        results = ilorest.run(['showdcpmmpendingconfig', '-h'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_no_flag(ilorest, dl360_large):
        """Test for the case when `showdcpmmpendingconfig` command is run without any flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmmpendingconfig'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_json_flag(ilorest, dl360_large):
        """Test for the case when `showdcpmmpendingconfig` command is run with json flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmmpendingconfig', '-j'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_extraneous_attributes(ilorest):
        """
        Test for the case when `showdcpmmpendingconfig` command is run with extraneous attributes
        """
        results = ilorest.run(['showdcpmmpendingconfig', '1qazxcsd'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

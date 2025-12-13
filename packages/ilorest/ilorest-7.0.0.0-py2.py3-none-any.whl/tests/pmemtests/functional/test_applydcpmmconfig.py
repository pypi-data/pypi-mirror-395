"""Module containing functional tests for the 'applydcpmmconfig' command"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestApplyPmemConfigCommand(object):
    """Class for functional tests for the applydcpmmconfig command"""

    @staticmethod
    def test_show_invalid_flag(ilorest):
        """Test function call with invalid flag"""
        results = ilorest.run(['applydcpmmconfig', '--bad-flag'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_show_help_flag(ilorest):
        """Test function call with help flag"""
        results = ilorest.run(['applydcpmmconfig', '-h'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_no_flag(ilorest):
        """Test for the case when `applydcpmmconfig` command is run without any flag"""
        results = ilorest.run(['applydcpmmconfig'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_force_flag_1(ilorest):
        """Test for the case when `applydcpmmconfig` command is run with force flag"""
        results = ilorest.run(['applydcpmmconfig', '-f'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_force_flag_2(ilorest):
        """Test for the case when `applydcpmmconfig` command is run with force flag"""
        results = ilorest.run(['applydcpmmconfig', '-L', '-f'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    # Cannot test for the positive case - mock server not accepting delete tasks.
    @staticmethod
    def test_with_force_flag_3(ilorest, dl360_large):
        """Test for the case when `applydcpmmconfig` command is run with force flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['applydcpmmconfig', '-C', 'MemoryMode', '-f'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.NO_CHANGES_MADE_OR_FOUND

    @staticmethod
    def test_with_config_flag_1(ilorest, dl360_large):
        """Test for the case when `applydcpmmconfig` command is run with config flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['applydcpmmconfig', '-C'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_config_flag_2(ilorest, dl360_large):
        """Test for the case when `applydcpmmconfig` command is run with config flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['applydcpmmconfig', '-C', 'xyz'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_config_flag_3(ilorest, dl360_large):
        """Test for the case when `applydcpmmconfig` command is run with config flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['applydcpmmconfig', '-C', 'AppDirectInterleaved'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.NO_CHANGES_MADE_OR_FOUND

    @staticmethod
    def test_with_list_flag(ilorest):
        """Test for the case when `applydcpmmconfig` command is run with list flag"""
        results = ilorest.run(['applydcpmmconfig', '-L'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_extra_attributes_1(ilorest):
        """Test for the case when `applydcpmmconfig` command is run with extraneous attributes"""
        results = ilorest.run(['applydcpmmconfig', '-L', '1qazxcsd'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_extra_attributes_2(ilorest, dl360_large):
        """Test for the case when `applydcpmmconfig` command is run with extraneous attributes"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['applydcpmmconfig', '-C', 'AppDirectInterleaved', '1qazxcsd'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

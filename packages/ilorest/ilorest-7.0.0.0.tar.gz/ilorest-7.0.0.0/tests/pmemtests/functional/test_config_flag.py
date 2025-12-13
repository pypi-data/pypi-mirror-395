"""Module containing functional tests for the config flag"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestConfigFlag(object):
    """Functional Tests for the --config | -C flag"""

    @staticmethod
    def test_with_no_dimm_id(ilorest, dl360_large):
        """Test for --config flag with no DIMM IDs specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_valid_dimm_id(ilorest, dl360_large):
        """Test for --config flag with valid DIMM IDs specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config', '--dimm', '1@2,2@3'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_non_pmem_dimm_id(ilorest, dl360_large):
        """Test for --config flag with valid non pmem DIMM IDs specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config', '--dimm', '1@5'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_json_format_1(ilorest, dl360_large):
        """Test for --config flag with --json flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config', '--dimm', '1@2,2@3', '-j'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_json_format_2(ilorest, dl360_large):
        """Test for --config flag with --json flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config', '-j'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_invalid_member_dimm_id(ilorest, dl360_large):
        """Test for --config flag with invalid DIMM IDs specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--config', '--dimm', '8@15'])
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_invalid_dimm_id(ilorest):
        """Test for --config flag with invalid DIMM IDs specified"""
        results = ilorest.run(['showdcpmm', '--config', '--dimm', '132,243,xyz'])
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

"""Module containing functional tests for the device flag"""
from __future__ import absolute_import

import sys

from rdmc_helper import ReturnCodes


class TestDeviceFlag(object):
    """Functional Tests for the --device | -D flag"""
    @staticmethod
    def test_with_no_dimm_id(ilorest, dl360_large):
        """Test for --device flag with no DIMM IDs specified"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_valid_non_pmem_dimm_id(ilorest, dl360_large):
        """
        Test for --device flag with valid DIMM IDs
        which are not Persistent Memory Modules specified
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device', '--dimm', '1@1,2@3'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_invalid_dimm_id_1(ilorest):
        """
        Test for --device flag with invalid DIMM IDs specified.
        Fails at Validation.
        """
        results = ilorest.run(['showdcpmm', '--device', '--dimm', '132,243,xyz'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_invalid_dimm_id_2(ilorest, dl360_large):
        """
        Test for --device flag with invalid DIMM IDs specified
        Passes Validation, Fails later when DIMM IDs not found
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device', '--dimm', '8@2,2@18'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_valid_pmem_dimm_id(ilorest, dl360_large):
        """
        Test for --device flag with valid DIMM IDs
        which are Persistent Memory Modules specified
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device', '--dimm', '1@2'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_valid_pmem_dimm_id_json(ilorest, dl360_large):
        """
        Test for --device flag with valid DIMM IDs
        which are Persistent Memory Modules specified
        along with the --json flag
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device', '--dimm', '1@2', '--json'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_json(ilorest, dl360_large):
        """
        Test for --device flag with valid DIMM IDs
        which are Persistent Memory Modules specified
        along with the --json flag
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--device', '--json'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

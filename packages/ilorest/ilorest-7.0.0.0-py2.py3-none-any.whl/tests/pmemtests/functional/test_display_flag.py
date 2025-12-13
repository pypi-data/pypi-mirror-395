"""Module containing functional tests for the device flag"""
from __future__ import absolute_import

import sys

import pytest

from rdmc_helper import ReturnCodes


@pytest.mark.skip(reason="temporarily remove display flag")
class TestDisplayFlag(object):
    """Functional Tests for the --display | -d flag"""

    @staticmethod
    def test_with_no_display_attributes(ilorest):
        """Test for --display flag with no display attributes"""
        results = ilorest.run(['showdcpmm', '--display'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_with_invalid_display_attributes(ilorest, dl360_large):
        """Test for --display flag with invalid display attributes"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--display', 'xyz,abc'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_valid_display_attributes(ilorest, dl360_large):
        """Test for --display flag with valid display attributes"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--display', 'DeviceLocator'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_with_valid_display_attributes_json(ilorest, dl360_large):
        """
        Test for --display flag with valid display attributes
        along with the --json flag
        """
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--display', 'DeviceLocator', '--json'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

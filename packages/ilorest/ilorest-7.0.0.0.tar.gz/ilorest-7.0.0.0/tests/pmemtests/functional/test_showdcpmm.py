"""
Functional tests for the command to show the DCPMMs
"""
from __future__ import absolute_import

import sys

import pytest
from jsonpointer import resolve_pointer
from pmemtests.functional.conftest import RestClient

from rdmc_helper import ReturnCodes


class TestShowDcPmemCommand(object):
    """Class for functional tests for the command to enable and disable the scalable pmem feature"""

    @staticmethod
    def test_show_invalid_flag(ilorest):
        """ test function call with invalid flag """
        results = ilorest.run(['showdcpmm', '--bad-flag'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_show_help_flag(ilorest):
        """ test function call with help flag """
        results = ilorest.run(['showdcpmm', '-h'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_showdcpmm_no_flag(ilorest, dl360_large):
        """Test for the case when `showdcpmm` command is run without any flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_showdcpmm_dimm_flag_1(ilorest):
        """Test for the case when `showdcpmm` command is run with dimm flag"""
        results = ilorest.run(['showdcpmm', '--dimm'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_showdcpmm_dimm_flag_2(ilorest, dl360_large):
        """Test for the case when `showdcpmm` command is run with dimm flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--dimm', '1@2'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

    @staticmethod
    def test_showdcpmm_dimm_flag_3(ilorest, dl360_large):
        """Test for the case when `showdcpmm` command is run with dimm flag"""
        url, username, password = dl360_large.config
        with ilorest.session(url, username, password):
            results = ilorest.run(['showdcpmm', '--dimm', '1@2', '2@3'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    @pytest.mark.skip(reason="temporarily remove display flag")
    def test_all_and_display_flags(ilorest):
        """Test for the case when --all and --display flags are specified together"""
        results = ilorest.run(['showdcpmm', '--all', '--display', 'xyz'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_device_and_config_flags(ilorest):
        """Test for the case when --device and --config flags are specified together"""
        results = ilorest.run(['showdcpmm', '--device', '--config'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_logical_and_summary_flags(ilorest):
        """Test for the case when --summary and --logical flags are specified together"""
        results = ilorest.run(['showdcpmm', '--logical', '--summary'])
        sys.stdout.write("results.stdout: ")
        sys.stdout.write(results.stdout)
        sys.stdout.write("results.stderr: ")
        sys.stdout.write(results.stderr)
        assert results.retcode == ReturnCodes.INVALID_COMMAND_LINE_ERROR

    @staticmethod
    def test_example(ilorest, dl360_large):
        """ this is just an example to show using the RestClient """
        url, username, password = dl360_large.config

        # run ilorest rawget
        with ilorest.session(url, username, password):
            results = ilorest.run(['rawget', '/redfish/v1/systems/1/bios/settings'])
            sys.stdout.write("results.stdout: ")
            sys.stdout.write(results.stdout)
            sys.stdout.write("results.stderr: ")
            sys.stdout.write(results.stderr)
            assert results.retcode == ReturnCodes.SUCCESS

        # check REST attributes
        client = RestClient(url, username, password)
        bios_settings = client.get('/redfish/v1/systems/1/bios/settings')
        sys.stdout.write(str(bios_settings))
        assert resolve_pointer(bios_settings, '/Attributes/MemFastTraining') == "Enabled"

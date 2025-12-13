"""
This module contains tests for ShowPmemCommand
"""
from __future__ import absolute_import

import pytest

from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import InvalidCommandLineError

from ..conftest import ShowPmemCommand


class CustomOptions(object):
    """
    Class to mock different options
    """

    def __init__(self):
        self.all = True
        self.display_attributes = None
        self.json = False

    def all_flag(self):
        """
        Function to set --all flag to true
        :return: CustomOptions object
        """
        self.all = True
        return self

    def no_flag(self):
        """
        Function to reset flags
        :return: CustomOptions object
        """
        self.all = False
        self.display_attributes = None
        return self

    def display_flag(self):
        """
        Function to set --display flag
        :return: CustomOptions object
        """
        self.all = False
        self.display_attributes = ["RandomNestedKey1"]
        return self

    def wrong_display_flag(self):
        """
        Function to set --display flag with wrong attributes
        :return: CustomOptions object
        """
        self.all = False
        self.display_attributes = ["aBc", "xYz"]
        return self

    @staticmethod
    def get_default(flag):
        """
        Function to return default attributes
        :return: list of attributes
        """
        if flag == "device":
            return ["Location", "SizeMiB"]
        if flag == "config":
            return ["Location", "Capacity"]
        return []

    @staticmethod
    def get_all(flag):
        """
        Function to return attributes for --all flag
        :return: list of attributes
        """
        if flag == "device":
            return ["Location", "SizeMiB", "RandomNestedKey1"]
        if flag == "config":
            return ["Location", "Capacity", "RandomNestedKey1"]
        return []


class MockMappingTable(object):
    """
    class to mock mapping table
    """
    memory = {'Capacity': {'path': '/CapacityMiB', 'redfishName': 'CapacityMiB'},
              'Location': {'path': '/DeviceLocator', 'redfishName': 'DeviceLocator'},
              'RandomAttribute': {'path': "/RandomAttribute",
                                  'redfishName': 'RandomAttribute'},
              'RandomNestedKey1': {'path': "/RandomAttribute/RandomNestedKey1",
                                   'redfishName': 'RandomNestedKey1'},
              'SizeMiB': {'path': '/Regions/SizeMiB', 'redfishName': 'SizeMiB'}}
    memorychunk = {'Capacity': {'path': '/CapacityMiB', 'redfishName': 'CapacityMiB'},
                   'Location': {'path': '/DeviceLocator', 'redfishName': 'DeviceLocator'},
                   'RandomAttribute': {'path': "/RandomAttribute",
                                       'redfishName': 'RandomAttribute'},
                   'RandomNestedKey1': {'path': "/RandomAttribute/RandomNestedKey1",
                                        'redfishName': 'RandomNestedKey1'},
                   'SizeMiB': {'path': '/Regions/SizeMiB', 'redfishName': 'SizeMiB'}}


class TestShowPmemCommands(object):
    """
    Class to test functions in ShowPmemCommands
    """
    mock_data = [
        {
            'DeviceLocator': 'PROC 1 DIMM 1',
            'CapacityMiB': 123456,
            'SizeMiB': 'xyz',
            'RandomAttribute': {
                'RandomNestedKey1': 'RandomNestedValue1.1',
                'RandomNestedKey2': [
                    'RandomNestedValue2.1',
                    'RandomNestedValue2.2'
                ],
                'RandomNestedKey4': [
                    {
                        'RandomNestedKey5': 'RandomNestedValue5.1'
                    }
                ]
            }
        },
        {
            'DeviceLocator': 'PROC 2 DIMM 12',
            'CapacityMiB': 987654,
            'SizeMiB': 'abc@123',
            'RandomAttribute': {
                'RandomNestedKey1': 'RandomNestedValue1.2',
                'RandomNestedKey2': [
                    'RandomNestedValue2.3',
                    'RandomNestedValue2.4'
                ],
                'RandomNestedKey4': [
                    {
                        'RandomNestedKey5': 'RandomNestedValue5.2'
                    }
                ]
            }
        }]

    custom_options_obj = CustomOptions()

    @pytest.mark.parametrize('members, options, flag, expected_output', [
        # display flag
        (mock_data, CustomOptions().display_flag(), "device",
         ['\nRandomNestedKey1: RandomNestedValue1.1', '\nRandomNestedKey1: RandomNestedValue1.2']),
        (mock_data, CustomOptions().display_flag(), "config",
         ['\nRandomNestedKey1: RandomNestedValue1.1', '\nRandomNestedKey1: RandomNestedValue1.2']),
        # no flag
        ([mock_data[1]], CustomOptions().no_flag(), "device",
         ['\nLocation: PROC 2 DIMM 12\nSizeMiB: None']),
        ([mock_data[0]], CustomOptions().no_flag(), "config",
         ['\nLocation: PROC 1 DIMM 1\nCapacity: 123456'])
    ])
    @pytest.mark.skip(reason="temporarily remove display flag")
    def test_generate_display_output_pass(self, members, options, flag, expected_output,
                                          monkeypatch):
        """
        Tests for generate_display_output() with valid input
        :param members: list of members returned as a result of GET request
        :param options: command options
        :param flag: name of flag
        :param expected_output: expected output of the test
        """
        monkeypatch.setattr(ShowPmemCommand, "get_default_attributes",
                            self.custom_options_obj.get_default)
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        result = pmem_command.generate_display_output(members, options, flag,
                                                      MockMappingTable.memory)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize('members, options, flag, expected_output', [
        ([mock_data[0]], CustomOptions().wrong_display_flag(), "device",
         ["\nNo match found for 'aBc'\nNo match found for 'xYz'"]),
        ([mock_data[1]], CustomOptions().wrong_display_flag(), "config",
         ["\nNo match found for 'aBc'\nNo match found for 'xYz'"]),
        (mock_data, CustomOptions().wrong_display_flag(), "config",
         ["\nNo match found for 'aBc'\nNo match found for 'xYz'",
          "\nNo match found for 'aBc'\nNo match found for 'xYz'"]),
    ])
    @pytest.mark.skip(reason="temporarily remove display flag")
    def test_generate_display_output_fail(members, options, flag, expected_output):
        """
        Tests for generate_display_output() with invalid input
        :param members: list of members returned as a result of GET request
        :param options: command options
        :param flag: name of flag
        :param expected_output: expected output of the test
        """
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        result = pmem_command.generate_display_output(members, options, flag,
                                                      MockMappingTable.memory)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize('customparser, expected_output', [
        ('', None)
    ])
    def test_define_arguments(customparser, expected_output):
        """
        Branch Test for definearguments() when parser is not customparser
        :param customparser: command line input
        :param expected_output: expected output of the test
        """
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        result = pmem_command.definearguments(customparser)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize("flag, expected_output", [
        ("device", ShowPmemCommand.DefaultAttributes.device.value),
        ("config", ShowPmemCommand.DefaultAttributes.config.value),
        ("summary", None),
        ("abc", None)])
    def test_get_default_attributes(flag, expected_output):
        """
        Test for get_default_attributes()
        :param flag: name of flag
        :param expected_output: expected output of the test
        """
        result = ShowPmemCommand.get_default_attributes(flag)
        assert result == expected_output


class MockOptions(object):
    """
    Class containing mock options for validation tests
    """
    device = False
    config = False
    summary = False
    logical = False
    dimm = None

    @staticmethod
    def set_options(device, config, logical, summary, dimm):
        """
        Setter method for Mock options
        """
        MockOptions.device = device
        MockOptions.config = config
        MockOptions.logical = logical
        MockOptions.summary = summary
        MockOptions.dimm = dimm


class TestValidation(object):
    """
    Class containing validation tests
    """
    @staticmethod
    @pytest.mark.parametrize("device, config, logical, summary, dimm, expected_result", [
        (False, False, False, False, None, None),
        (False, False, False, False, ["1@1", "2@10"], None),
        (True, False, False, False, None, None),
        (True, False, False, False, ["3@12", "4@8"], None),
        (False, True, False, False, None, None),
        (True, False, False, False, ["4@4", "3@3"], None),
        (True, False, False, False, ["9@19"], None),
        (False, False, True, False, None, None),
        (False, False, False, True, None, None)
    ])
    def test_validate_show_pmem_options_pass(device, config, logical,
                                             summary, dimm, expected_result):
        """
        Tests for 'validate_options' with valid options
        """
        MockOptions.set_options(device, config, logical, summary, dimm)
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        result = pmem_command.validate_show_pmem_options(MockOptions)
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize("device, config, logical, summary, dimm", [
        (True, True, True, True, None),
        (True, True, True, False, None),
        (True, True, False, True, None),
        (True, False, True, True, None),
        (False, True, True, True, None),
        (True, True, False, False, None),
        (True, False, True, False, None),
        (True, False, False, True, None),
        (False, False, True, True, None),
        (False, True, False, True, None),
        (False, True, True, False, None),
        (True, False, False, False, ["0@0"]),
        (True, False, False, False, ["0@8"]),
        (True, False, False, False, ["4@0"]),
        (True, False, False, False, ["4@20"]),
        (True, False, False, False, ["10@20"]),
        (True, False, False, False, ["10@2"]),
        (True, False, False, False, ["3)12", "438"]),
        (True, False, False, False, ["4#4", "3!3"]),
        (True, False, False, False, ["3)12", "438"]),
        (False, False, False, False, ["1@1", "2@=10"]),
        (False, False, True, False, ["3@12", "4@8"]),
        (False, False, False, True, ["4@4", "3@3"])
    ])
    def test_validate_show_pmem_options_fail(device, config, logical, summary, dimm):
        """
        Tests for 'validate_options' with invalid options
        """
        MockOptions.set_options(device, config, logical, summary, dimm)
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        with pytest.raises(InvalidCommandLineError):
            pmem_command.validate_show_pmem_options(MockOptions)

    @staticmethod
    @pytest.mark.parametrize("device, config, logical, summary, dimm", [
        (False, False, False, False, None),
        (False, False, False, False, ["1@2"]),
        (True, False, False, False, None),
        (True, False, False, False, ["4#4", "3!3"]),
        (False, True, False, False, None),
        (False, True, False, False, ["4@4", "3@3"]),
        (False, False, True, False, None),
        (False, False, True, False, ["1@1", "2@=10"]),
        (False, False, False, True, None),
        (False, False, False, True, ["1@1", "2@10"])
    ])
    def test_validate_args(device, config, logical, summary, dimm):
        """
        Tests for 'validate_args'
        """
        MockOptions.set_options(device, config, logical, summary, dimm)
        pmem_command = ShowPmemCommand.ShowPmemCommand(RdmcCommandBase)
        with pytest.raises(InvalidCommandLineError):
            pmem_command.validate_args(MockOptions)

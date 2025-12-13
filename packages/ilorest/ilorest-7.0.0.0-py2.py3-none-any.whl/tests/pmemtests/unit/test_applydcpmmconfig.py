"""Module to Test the 'applydcpmmconfig' command"""
from __future__ import absolute_import

import pytest

from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import (
    InvalidCommandLineError,
    NoChangesFoundOrMadeError,
    NoContentsFoundForOperationError,
)

from ..conftest import ApplyPmemConfigCommand, RestHelpers


class MockData(object):
    """
    Mock Data for 'applydcpmmconfig' command
    """
    mock_tasks = [{
        "@odata.context": "/redfish/v1/$metadata#Task.Task",
        "Name": "Task 1",
        "Payload": {
            "HttpOperation": "POST",
            "JsonBody": "{\"AddressRangeType\": \"PMEM\","
                        "\"InterleaveSets\": "
                        "[{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc1dimm1/\"}},"
                        "{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc1dimm12/\"}}],"
                        "\"Oem\": {\"Hpe\": {\"MemoryChunkSizePercentage\": 0}}}",
            "TargetUri": "/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/"
                         "MemoryChunks/?$expand=."
        },
        "TaskState": "New"
    }, {
        "@odata.context": "/redfish/v1/$metadata#Task.Task",
        "Name": "Task 2",
        "Payload": {
            "HttpOperation": "POST",
            "JsonBody": "{\"AddressRangeType\": \"PMEM\","
                        "\"InterleaveSets\": "
                        "[{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc2dimm1/\"}},"
                        "{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc2dimm10/\"}}],"
                        "\"Oem\": {\"Hpe\": {\"MemoryChunkSizePercentage\": 0}}}",
            "TargetUri": "/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/"
                         "MemoryChunks/?$expand=."
        },
        "TaskState": "Old"
    }]

    other_mock_tasks = [{
        "@odata.context": "/redfish/v1/$metadata#Task.Task",
        "Name": "Task 1",
        "Payload": {
            "HttpOperation": "POST",
            "JsonBody": "{\"AddressRangeType\": \"PMEM\","
                        "\"InterleaveSets\": "
                        "[{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc1dimm1/\"}},"
                        "{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc1dimm12/\"}}],"
                        "\"Oem\": {\"Hpe\": {\"MemoryChunkSizePercentage\": 0}}}",
            "TargetUri": "/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/?$expand=."
        },
        "TaskState": "New"
    }, {
        "@odata.context": "/redfish/v1/$metadata#Task.Task",
        "Name": "Task 2",
        "Payload": {
            "HttpOperation": "POST",
            "JsonBody": "{\"AddressRangeType\": \"PMEM\","
                        "\"InterleaveSets\": "
                        "[{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc2dimm1/\"}},"
                        "{\"Memory\": "
                        "{\"@odata.id\": \"/redfish/v1/Systems/1/Memory/proc2dimm10/\"}}],"
                        "\"Oem\": {\"Hpe\": {\"MemoryChunkSizePercentage\": 0}}}",
            "TargetUri": "/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/?$expand=."
        },
        "TaskState": "Old"
    }]

    mock_chunks = [
        {
            "@odata.context": "/redfish/v1/$metadata#MemoryChunks.MemoryChunks",
            "@odata.etag": "W/\"89E7F7C3\"",
            "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/MemoryChunks/2/",
            "@odata.type": "#MemoryChunks.v1_2_2.MemoryChunks",
            "Id": "2",
            "AddressRangeType": "PMEM",
            "Description": "Memory Chunk",
            "InterleaveSets": [
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm7/"
                    },
                    "RegionId": "3",
                    "SizeMiB": 131072
                }
            ],
            "IsMirrorEnabled": False,
            "IsSpare": False,
            "MemoryChunkSizeMiB": 131072,
            "Name": "MemoryChunk",
            "Oem": {
                "Hpe": {
                    "@odata.context": "/redfish/v1/$metadata#HpeMemoryChunksExt.HpeMemoryChunksExt",
                    "@odata.type": "#HpeMemoryChunksExt.v2_1_0.HpeMemoryChunksExt",
                    "MemoryChunkSizePercentage": 50
                }
            }
        },
        {
            "@odata.context": "/redfish/v1/$metadata#MemoryChunks.MemoryChunks",
            "@odata.etag": "W/\"89E7F7C3\"",
            "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/MemoryChunks/1/",
            "@odata.type": "#MemoryChunks.v1_2_2.MemoryChunks",
            "Id": "1",
            "AddressRangeType": "PMEM",
            "Description": "Memory Chunk",
            "InterleaveSets": [
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm6/"
                    },
                    "RegionId": "1",
                    "SizeMiB": 131072
                }
            ],
            "IsMirrorEnabled": False,
            "IsSpare": False,
            "MemoryChunkSizeMiB": 131072,
            "Name": "MemoryChunk",
            "Oem": {
                "Hpe": {
                    "@odata.context": "/redfish/v1/$metadata#HpeMemoryChunksExt.HpeMemoryChunksExt",
                    "@odata.type": "#HpeMemoryChunksExt.v2_1_0.HpeMemoryChunksExt",
                    "MemoryChunkSizePercentage": 50
                }
            }
        }
    ]

    mock_interleavable_set = [
        {
            "MemorySet": [
                {
                    "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm6/"
                },
                {
                    "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm7/"
                }
            ]
        },
        {
            "MemorySet": [
                {
                    "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm6/"
                }
            ]
        },
        {
            "MemorySet": [
                {
                    "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm7/"
                }
            ]
        }
    ]

    expect_post_bodies_app_direct_interleaved = [
        {
            'AddressRangeType': 'PMEM',
            'Oem': {
                'Hpe': {
                    'MemoryChunkSizePercentage': 100
                }
            },
            'InterleaveSets': [
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'
                    }
                },
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'
                    }
                }
            ]
        }
    ]

    expected_post_bodies_app_direct_not_interleaved = [
        {
            'AddressRangeType': 'PMEM',
            'Oem': {
                'Hpe': {
                    'MemoryChunkSizePercentage': 100
                }
            },
            'InterleaveSets': [
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'
                    }
                }
            ]
        },
        {
            'AddressRangeType': 'PMEM',
            'Oem': {
                'Hpe': {
                    'MemoryChunkSizePercentage': 100
                }
            },
            'InterleaveSets': [
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'
                    }
                }
            ]
        }
    ]

    expected_post_bodies_memory_mode = [
        {
            'AddressRangeType': 'PMEM',
            'Oem': {
                'Hpe': {
                    'MemoryChunkSizePercentage': 0
                }
            },
            'InterleaveSets': [
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'
                    }
                },
                {
                    'Memory': {
                        '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'
                    }
                }
            ]
        }

    ]

    def retrieve_memory_domains(self):
        """
        Function to retrive memory domains
        """
        memory_domains = [{
            'Name': 'PROC1 Memory Domain',
            '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain',
            '@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
            'Id': 'PROC1MemoryDomain',
            "InterleavableMemorySets":[{
                "MemorySet":[
                    {
                        "@odata.id":"/redfish/v1/Systems/1/Memory/proc2dimm6/"
                    },
                    {
                        "@odata.id":"/redfish/v1/Systems/1/Memory/proc2dimm7/"
                    }
                ]
            }, {
                "MemorySet":[
                    {
                        "@odata.id":"/redfish/v1/Systems/1/Memory/proc2dimm6/"
                    }
                ]
            }, {
                "MemorySet":[
                    {
                        "@odata.id":"/redfish/v1/Systems/1/Memory/proc2dimm7/"
                    }
                ]
            }],
            "MemoryChunks":{
                "@odata.id":"/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/MemoryChunks"}
        }]
        return [], memory_domains, []

class TestApplyPmemConfigCommand(object):
    """
    Class for unit tests of 'applydcpmmconfig' command
    """

    @staticmethod
    @pytest.mark.parametrize('customparser, expected_result', [
        ('', None)
    ])
    def test_define_arguments(customparser, expected_result):
        """
        Branch Test for 'define_arguments()' when parser is not customparser
        """
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(
            RdmcCommandBase)
        result = pmem_command.define_arguments(customparser)
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize('memory_chunk_tasks, memory_chunks', [
        ([MockData.mock_tasks[0]], list()),
        (list(), MockData.mock_chunks),
        ([MockData.mock_tasks[1]], MockData.mock_chunks),
        ([MockData.other_mock_tasks[0]], MockData.mock_chunks)
    ])
    def test_warn_existing_chunks_and_tasks_fail(memory_chunk_tasks, memory_chunks):
        """
        Tests for 'delete_existing_chunks_and_tasks' with invalid data
        """
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        with pytest.raises(NoChangesFoundOrMadeError):
            pmem_command.warn_existing_chunks_and_tasks(memory_chunk_tasks, memory_chunks)

    @staticmethod
    @pytest.mark.parametrize('memory_chunk_tasks, memory_chunks, expected_result', [
        (list(), list(), None),
        (None, list(), None)
    ])
    def test_warn_existing_chunks_and_tasks_pass(memory_chunk_tasks,
                                                 memory_chunks, expected_result):
        """
        Tests for 'delete_existing_chunks_and_tasks' with valid data
        """
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        result = pmem_command.warn_existing_chunks_and_tasks(memory_chunk_tasks, memory_chunks)
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize('memory_chunk_tasks, memory_chunks, response, expected_result', [
        ([MockData.mock_tasks[0]], list(), 200, None),
        ([MockData.mock_tasks[0]], MockData.mock_chunks, 202, None),
        (None, None, None, None),
        (list(), list(), None, None)
    ])
    def test_delete_existing_chunks_and_tasks_pass(memory_chunk_tasks, memory_chunks,
                                                   response, expected_result, monkeypatch):
        """
        Tests for 'delete_existing_chunks_and_tasks' with valid data
        """
        def get_response(*argv):
            """
            Returns response codes
            """
            #pylint: disable=unused-argument
            return response
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource", get_response)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        result = pmem_command.delete_existing_chunks_and_tasks(memory_chunk_tasks, memory_chunks)
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize('memory_chunk_tasks, memory_chunks', [
        ([MockData.mock_tasks[0]], MockData.mock_chunks),
        (None, MockData.mock_chunks),
    ])
    def test_delete_existing_chunks_and_tasks_fail(memory_chunk_tasks, memory_chunks, monkeypatch):
        """
        Tests for 'delete_existing_chunks_and_tasks' with invalid data
        """
        def get_response(*argv):
            """
            Returns none
            """
            #pylint: disable=unused-argument
            return None
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource", get_response)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        with pytest.raises(NoChangesFoundOrMadeError):
            pmem_command.delete_existing_chunks_and_tasks(memory_chunk_tasks, memory_chunks)


class MockOptions(object):
    """
    Class containing mock options for validation tests
    """
    list = False
    config = ""
    force = False

    @staticmethod
    def set_options(list, config, force):
        """
        Setter function for options
        """
        MockOptions.list = list
        MockOptions.config = config
        MockOptions.force = force


class TestValidation(object):
    """
    Class containing test for validation based on mock options
    """
    @staticmethod
    @pytest.mark.parametrize("list, config, force, expected_result", [
        (True, False, False, None),
        (False, "memorymode", False, None),
        (False, "appdirectnotinterleaved", True, None),
        (False, "appdirectinterleaved", True, None),
        (False, "AppdirecTinterLeaveD", False, None),
        (False, "APPDIRECTNOTINTERLEAVED", False, None),
    ])
    def test_validate_options_pass(list, config, force, expected_result):
        """
        Tests for 'validate_options' with valid options
        """
        MockOptions.set_options(list, config, force)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        result = pmem_command.validate_options(MockOptions)
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize("list_flag, config, force", [
        (False, "", False),
        (True, "AppDirectInterleaved", False),
        (False, "qwerty", True),
        (True, "MemoryMode", True),
        (False, None, True),
        (True, None, True)
    ])
    def test_validate_options_fail(list_flag, config, force):
        """
        Tests for 'validate_options' with invalid options
        """
        MockOptions.set_options(list_flag, config, force)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        with pytest.raises(InvalidCommandLineError):
            pmem_command.validate_options(MockOptions)

    @staticmethod
    @pytest.mark.parametrize("list_flag, config, force", [
        (False, "False", False),
        (False, None, True),
        (True, "args", True)
    ])
    def test_validate_args(list_flag, config, force):
        """
        Tests for 'validate_args'
        """
        MockOptions.set_options(list_flag, config, force)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        with pytest.raises(InvalidCommandLineError):
            pmem_command.validate_args(MockOptions)

    @staticmethod
    @pytest.mark.parametrize('mock_config_data, mock_interleavable_set, expected_result', [
        (ApplyPmemConfigCommand.ApplyPmemConfigCommand.config_ids[0],
         MockData.mock_interleavable_set,
         MockData.expected_post_bodies_memory_mode),
        (ApplyPmemConfigCommand.ApplyPmemConfigCommand.config_ids[1],
         MockData.mock_interleavable_set,
         MockData.expect_post_bodies_app_direct_interleaved),
        (ApplyPmemConfigCommand.ApplyPmemConfigCommand.config_ids[2],
         MockData.mock_interleavable_set,
         MockData.expected_post_bodies_app_direct_not_interleaved)
    ])

    def test_get_post_data(mock_config_data, mock_interleavable_set, expected_result):
        """
        Test for get_post_data with MemoryMode, AppDirectInterleaved and AppDirectNotInterleaved
        """
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(
            RdmcCommandBase)
        result = pmem_command.get_post_data(mock_config_data, mock_interleavable_set)
        assert result == expected_result

    @staticmethod
    def test_apply_predefined_err(monkeypatch):
        """
        Test for apply_predefined_config with empty memory domains list
        """
        def retrive_empty_mem_domains(*argv):
            """
            returns empty list
            """
            #pylint: disable=unused-argument
            return [], [], []

        MockOptions.set_options(False, "memorymode", True)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        monkeypatch.setattr(RestHelpers.RestHelpers, "retrieve_task_members_and_mem_domains",
                            retrive_empty_mem_domains)
        with pytest.raises(NoContentsFoundForOperationError):
            pmem_command.apply_predefined_config(MockOptions)

    def test_apply_predefined_err3(self, monkeypatch):
        """
        Test for apply_predefined_config with invalid post request
        """
        def get_failure_resp(*argv):
            """
            returns None
            """
            #pylint: disable=unused-argument
            return None
        MockOptions.set_options(False, "appdirectinterleaved", True)
        pmem_command = ApplyPmemConfigCommand.ApplyPmemConfigCommand(RdmcCommandBase)
        monkeypatch.setattr(RestHelpers.RestHelpers, "retrieve_task_members_and_mem_domains",
                            MockData().retrieve_memory_domains)
        monkeypatch.setattr(RestHelpers.RestHelpers, "post_resource", get_failure_resp)
        with pytest.raises(NoChangesFoundOrMadeError):
            pmem_command.apply_predefined_config(MockOptions)

"""Module to Test the 'cleardcpmmpendingconfig' command"""
from __future__ import absolute_import

import pytest

from rdmc_base_classes import RdmcCommandBase
from rdmc_helper import NoChangesFoundOrMadeError, NoContentsFoundForOperationError

from .conftest import ClearPendingConfigCommand, RestHelpers


class MockData(object):
    """
    Mock Data for 'cleardcpmmpendingconfig' command
    """
    task = None
    resp = None

    mock_tasks_1 = [{
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

    mock_tasks_2 = [{
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
    }]

    mock_tasks_3 = [{
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

    @staticmethod
    def get_resource_tasks(*argv):
        """
        Returns mock tasks
        """
        return MockData.task

    @staticmethod
    def get_response_code(*argv):
        """
        Returns mock response codes
        """
        return MockData.resp

class TestDeleteTasks(object):
    """
    Class for unit tests of 'cleardcpmmpendingconfig' command
    """

    @staticmethod
    @pytest.mark.parametrize("tasks, expected_result", [
        (MockData.mock_tasks_1, [MockData.mock_tasks_1[0]]),
        ([MockData.mock_tasks_2[0]], [MockData.mock_tasks_2[0]])
    ])
    def test_get_memory_chunk_tasks_pass(tasks, expected_result, monkeypatch):
        """
        Tests for 'get_memory_chunk_tasks' with valid data
        """
        MockData.task = tasks
        monkeypatch.setattr(RestHelpers.RestHelpers,
                            "retrieve_task_members", MockData.get_resource_tasks)
        pmem_command = ClearPendingConfigCommand.ClearPendingConfigCommand(RdmcCommandBase)
        result = pmem_command.get_memory_chunk_tasks()
        assert result == expected_result

    @staticmethod
    @pytest.mark.parametrize("tasks", [
        (MockData.mock_tasks_3),
        ([MockData.mock_tasks_3[0]]),
        ([MockData.mock_tasks_3[1]]),
        ([MockData.mock_tasks_1[1]])
    ])
    def test_get_memory_chunk_tasks_fail(tasks, monkeypatch):
        """
        Tests for 'get_memory_chunk_tasks' with invalid data
        """
        MockData.task = tasks
        monkeypatch.setattr(RestHelpers.RestHelpers, "retrieve_task_members",
                            MockData.get_resource_tasks)
        pmem_command = ClearPendingConfigCommand.ClearPendingConfigCommand(RdmcCommandBase)
        with pytest.raises(NoContentsFoundForOperationError):
            pmem_command.get_memory_chunk_tasks()

    @staticmethod
    @pytest.mark.parametrize("resp, verbose", [
        (200, False),
        (200, True)
    ])
    def test_delete_tasks_pass(resp, verbose, monkeypatch):
        """
        Tests for 'delete_tasks' with valid data
        """
        MockData.resp = resp
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource",
                            MockData.get_response_code)
        pmem_command = ClearPendingConfigCommand.ClearPendingConfigCommand(RdmcCommandBase)
        result = pmem_command.delete_tasks(MockData.mock_tasks_3, verbose)
        assert result is None

    @staticmethod
    @pytest.mark.parametrize("resp, verbose", [
        (None, False),
        (None, True)
    ])
    def test_delete_tasks_fail(resp, verbose, monkeypatch):
        """
        Tests for 'delete_tasks' with invalid data
        """
        MockData.resp = resp
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource",
                            MockData.get_response_code)
        pmem_command = ClearPendingConfigCommand.ClearPendingConfigCommand(RdmcCommandBase)
        with pytest.raises(NoChangesFoundOrMadeError):
            pmem_command.delete_tasks(MockData.mock_tasks_3, verbose)

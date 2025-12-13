"""Module to Test the Rest Helpers Class"""
from __future__ import absolute_import

import pytest

from rdmc_base_classes import RdmcCommandBase

from .conftest import RestHelpers


class MockMemoryDomainResource(object):
    """
    Class to mock Memory Domain Resources
    """

    def __init__(self):
        self.status = 200
        self.dict = {"@odata.context": "/redfish/v1/$metadata#MemoryDomainCollection"
                                       ".MemoryDomainCollection",
                     "@odata.etag": "W\"92240A75\"",
                     "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/",
                     "@odata.type": "#MemoryDomainCollection.MemoryDomainCollection",
                     "Description": "Memory Domains Collection",
                     "Members": [{"@odata.context": "/redfish/v1/$metadata#MemoryDomain."
                                                    "MemoryDomain",
                                  "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/"
                                               "PROC1MemoryDomain/",
                                  "@odata.type": "#MemoryDomain.v1_0_0.MemoryDomain",
                                  "Id": "PROC1MemoryDomain",
                                  "InterleavableMemorySets": [
                                      {"MemorySet": [{"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                                   "proc1dimm6/"},
                                                     {"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                                   "proc1dimm7/"}]},
                                      {"MemorySet": [{"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                                   "proc1dimm6/"}]},
                                      {"MemorySet": [{"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                                   "proc1dimm7/"}]}],
                                  "MemoryChunks": {
                                      "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/"
                                                   "PROC1MemoryDomain/MemoryChunks/"},
                                  "Name": "PROC1 Memory Domain"},
                                 {
                                     "@odata.context": "/redfish/v1/$metadata#MemoryDomain"
                                                       ".MemoryDomain",
                                     "@odata.id": "/redfish/v1/Systems/1/MemoryDomains"
                                                  "/PROC2MemoryDomain/",
                                     "@odata.type": "#MemoryDomain.v1_0_0.MemoryDomain",
                                     "Id": "PROC2MemoryDomain",
                                     "InterleavableMemorySets": [
                                         {"MemorySet": [
                                             {"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                           "proc2dimm6/"},
                                             {"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                           "proc2dimm7/"}]},
                                         {"MemorySet": [
                                             {"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                           "proc2dimm6/"}]},
                                         {"MemorySet": [
                                             {"@odata.id": "/redfish/v1/Systems/1/Memory/"
                                                           "proc2dimm7/"}]}],
                                     "MemoryChunks": {
                                         "@odata.id": "/redfish/v1/Systems/1/MemoryDomains/"
                                                      "PROC2MemoryDomain/MemoryChunks/"},
                                     "Name": "PROC2 Memory Domain"}],
                     "Members@odata.count": 2,
                     "Name": "Memory Domains Collection"}

    def get_obj(self, *argv):
        """
        Returns dict
        """
        return self.dict


class MockTaskResources(object):
    """
    Class to mock Task Resources
    """
    Tasks = [{
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

    Other_Tasks = [{
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
        Returns valid Task resources
        """
        return {"Members": MockTaskResources.Tasks}

    @staticmethod
    def get_resource_empty(*argv):
        """
        Returns empty Task Resources
        """
        return {"Members": []}

    @staticmethod
    def get_resource_none(*argv):
        """
        returns None
        """
        return None


class TestRestHelpers(object):
    """
    Class to test methods from the RestHelpers class
    """

    @staticmethod
    def test_retrieve_mem_domain_resources(monkeypatch):
        """
        Test for retrieving Memory Domain Resources
        """
        monkeypatch.setattr(RestHelpers.RestHelpers,
                            "get_resource", MockMemoryDomainResource().get_obj)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.retrieve_mem_domain_resources()
        assert resp == ([{'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC1MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]},
                              {'MemorySet': [{
                                  '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'}]},
                              {'MemorySet': [{
                                  '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC1 Memory Domain'},
                         {'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC2MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]},
                              {'MemorySet': [{
                                  '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'}]},
                              {'MemorySet': [{
                                  '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC2 Memory Domain'}],
                        [{'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC1MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]},
                              {'MemorySet': [
                                  {
                                      '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'}]},
                              {'MemorySet': [
                                  {
                                      '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC1 Memory Domain'},
                         {'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC2MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]},
                              {'MemorySet': [
                                  {
                                      '@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'}]},
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC2 Memory Domain'},
                         {'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC1MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]},
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm6/'}]},
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC1MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC1 Memory Domain'},
                         {'@odata.context': '/redfish/v1/$metadata#MemoryDomain.MemoryDomain',
                          '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain/',
                          '@odata.type': '#MemoryDomain.v1_0_0.MemoryDomain',
                          'Id': 'PROC2MemoryDomain',
                          'InterleavableMemorySets': [
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'},
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]},
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm6/'}]},
                              {'MemorySet': [
                                  {'@odata.id': '/redfish/v1/Systems/1/Memory/proc2dimm7/'}]}],
                          'MemoryChunks': {
                              '@odata.id': '/redfish/v1/Systems/1/MemoryDomains/PROC2MemoryDomain'
                                           '/MemoryChunks/'},
                          'Name': 'PROC2 Memory Domain'}])

    @staticmethod
    @pytest.mark.parametrize('mock_get_resource, expected_output', [
        (MockTaskResources.get_resource_tasks, MockTaskResources.Tasks),
        (MockTaskResources.get_resource_empty, []),
        (MockTaskResources.get_resource_none, [])
    ])
    def test_retrieve_task_members(mock_get_resource, expected_output, monkeypatch):
        """
        Tests for retrieving task members
        """
        monkeypatch.setattr(RestHelpers.RestHelpers,
                            "get_resource", mock_get_resource)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.retrieve_task_members()
        assert resp == expected_output

    @staticmethod
    @pytest.mark.parametrize("task_members, expected_output", [
        (MockTaskResources.Tasks, [MockTaskResources.Tasks[0]]),
        ([MockTaskResources.Tasks[1]], []),
        (MockTaskResources.Other_Tasks, []),
        ([MockTaskResources.Other_Tasks[0]], []),
        ([MockTaskResources.Other_Tasks[1]], []),
        ([], [])
    ])
    def test_filter_task_members(task_members, expected_output):
        """
        Tests for filtering task members
        """
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.filter_task_members(task_members)
        assert resp == expected_output


class MockDeleteResponse(object):
    """
    Class to Mock Delete Response
    """
    @staticmethod
    def get_success_resp(*argv):
        """
        Returns a success response code (200)
        """
        return 200

    @staticmethod
    def get_failure_resp(*argv):
        """
        Returns a failure response code (200)
        """
        return 400


class TestDeleteResponse(object):
    """
    Class to Test Delete Response
    """
    @staticmethod
    def test_delete_success(monkeypatch):
        """
        Test where deletion is successful
        """
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource",
                            MockDeleteResponse().get_success_resp)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.delete_resource("/redfish/v1/TaskService/Tasks/1")
        assert resp == 200

    @staticmethod
    def test_delete_failure(monkeypatch):
        """
        Test where deletion fails
        """
        monkeypatch.setattr(RestHelpers.RestHelpers, "delete_resource",
                            MockDeleteResponse().get_failure_resp)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.delete_resource("/redfish/v1/TaskService/Tasks/1")
        assert resp == 400


class MockPostResponse(object):
    """
    Class to Mock Post Response
    """

    @staticmethod
    def get_success_resp(*argv):
        """
        Returns a success response code (202)
        """
        return 202

    @staticmethod
    def get_failure_resp(*argv):
        """
        Returns a failure response code (402)
        """
        return 402


class TestPostResponse(object):
    """
    Class to Test Post Response
    """

    @staticmethod
    def test_post_success(monkeypatch):
        """
        Test where POST succeds
        """
        monkeypatch.setattr(RestHelpers.RestHelpers,
                            "post_resource", MockPostResponse().get_success_resp)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.post_resource(
            "/redfish/v1/TaskService/Tasks/1", {"default": "testing"})
        assert resp == 202

    @staticmethod
    def test_post_failure(monkeypatch):
        """
        Test where POST fails
        """
        monkeypatch.setattr(RestHelpers.RestHelpers,
                            "post_resource", MockPostResponse().get_failure_resp)
        rest_helpers = RestHelpers.RestHelpers(RdmcCommandBase)
        resp = rest_helpers.post_resource(
            "/redfish/v1/TaskService/Tasks/1", {"default": "testing"})
        assert resp == 402

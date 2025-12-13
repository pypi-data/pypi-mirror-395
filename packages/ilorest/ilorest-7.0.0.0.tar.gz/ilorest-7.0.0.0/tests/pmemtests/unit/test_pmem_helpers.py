"""
This module contains tests for PmemHelpers
"""
from __future__ import absolute_import

import pytest

from ..conftest import PmemHelpers


class TestPmemHelpers(object):
    """
    Class to test functions in PmemHelpers
    """
    mem_members = [
        {
            "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm1/",
            "DeviceLocator": "PROC 1 DIMM 1",
            "MemoryType": "NVDIMM_P",
            "Oem": {
                "Hpe": {
                    "@odata.context": "/redfish/v1/$metadata#HpeMemoryExt.HpeMemoryExt",
                    "@odata.type": "#HpeMemoryExt.v2_1_0.HpeMemoryExt",
                    "ProductName": "Intel Optane Memory"
                }
            }
        },
        {
            "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm2/",
            "DeviceLocator": "PROC 1 DIMM 2",
            "MemoryType": "DRAM",
            "Oem": {
                "Hpe": {
                    "@odata.context": "/redfish/v1/$metadata#HpeMemoryExt.HpeMemoryExt",
                    "@odata.type": "#HpeMemoryExt.v2_1_0.HpeMemoryExt",
                    "DIMMStatus": "NotPresent"
                }
            }
        }
    ]

    chunks = [
        {
            "InterleaveSets": [
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm1/"
                    }
                }
            ]
        },
        {
            "InterleaveSets": [
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc1dimm12/"
                    }
                }
            ]
        },
        {
            "InterleaveSets": [
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm1/"
                    }
                },
                {
                    "Memory": {
                        "@odata.id": "/redfish/v1/Systems/1/Memory/proc2dimm12/"
                    },
                }
            ]
        }
    ]

    @staticmethod
    @pytest.mark.parametrize('dimm_id_list, expected_output', [
        (['1@2', '2@3', '3@4'], ['PROC 1 DIMM 2', 'PROC 2 DIMM 3', 'PROC 3 DIMM 4']),
        (['2@12'], ['PROC 2 DIMM 12'])
    ])
    def test_parse_dimm_id(dimm_id_list, expected_output):
        """
        Test for parse_dimm_id()
        :param dimm_id_list: DIMM IDs in the 'X@Y' format
        :param expected_output: expected output of the test
        """
        result = PmemHelpers.PmemHelpers.parse_dimm_id(dimm_id_list)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize("memory_members, expected_output", [
        (mem_members, ([{'MemoryType': 'NVDIMM_P',
                         '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm1/',
                         'Oem': {
                             'Hpe':
                                 {'@odata.type': '#HpeMemoryExt.v2_1_0.HpeMemoryExt',
                                  '@odata.context': '/redfish/v1/$metadata#HpeMemoryExt.'
                                                    'HpeMemoryExt',
                                  'ProductName': 'Intel Optane Memory'}
                         },
                         'DeviceLocator': 'PROC 1 DIMM 1'}],
                       set(['PROC 1 DIMM 1']))),
        ([mem_members[0]], ([{'MemoryType': 'NVDIMM_P',
                              '@odata.id': '/redfish/v1/Systems/1/Memory/proc1dimm1/',
                              'Oem': {
                                  'Hpe':
                                      {'@odata.type': '#HpeMemoryExt.v2_1_0.HpeMemoryExt',
                                       '@odata.context': '/redfish/v1/$metadata#HpeMemoryExt.'
                                                         'HpeMemoryExt',
                                       'ProductName': 'Intel Optane Memory'}
                              },
                              'DeviceLocator': 'PROC 1 DIMM 1'}],
                            set(['PROC 1 DIMM 1']))),
        ([mem_members[1]], ([], set([]))),
        ([], ([], set([])))
    ])
    def test_get_pmem_members(memory_members, expected_output):
        """
        Test for get_pmem_members()
        :param memory_members: members of memory collection resource
        :param expected_output: expected output of the test
        """
        result = PmemHelpers.PmemHelpers.get_pmem_members(memory_members)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize("data_id, chunks, expected_output", [
        ("/redfish/v1/Systems/1/Memory/proc1dimm1/", chunks, False),
        ("/redfish/v1/Systems/1/Memory/proc2dimm1/", chunks, True),
        ("/redfish/v1/Systems/1/Memory/proc2dimm1/", [], None),
        ("/redfish/v1/Systems/1/Memory/proc1dimm4/", chunks, None)])
    def test_is_interleave_set(data_id, chunks, expected_output):
        """
        Test for is_interleave_set()
        :param data_id: @odata.id of the memory to be checked
        :param chunks: list of chunks
        :param expected_output: expected output of the test
        """
        result = PmemHelpers.PmemHelpers.is_interleave_set(data_id, chunks)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize('location_list, expected_output', [
        (['PROC X DIMM Y'], ('X@Y', 'PROC X')),
        (['PROC A DIMM B', 'PROC A DIMM C', 'PROC A DIMM D'], ('A@B, A@C, A@D', 'PROC A'))
    ])
    def test_location_format_converter(location_list, expected_output):
        """
        Test for location_format_converter()
        :param location_list: list of locations of the format 'PROC X DIMM Y'
        :param expected_output: expected output of the test
        """
        result = PmemHelpers.PmemHelpers.location_format_converter(location_list)
        assert result == expected_output

    @staticmethod
    @pytest.mark.parametrize("id1, id2, expected_output", [
        ("/redfish/v1/Systems/1/Memory/proc1dimm1", "/redfish/v1/Systems/1/Memory/proc1dimm1",
         True),
        ("/redfish/v1/Systems/1/Memory/proc1dimm1/", "/redfish/v1/Systems/1/Memory/proc1dimm1",
         True),
        ("/redfish/v1/Systems/1/Memory/proc1dimm1", "/redfish/v1/Systems/1/Memory/proc1dimm1/",
         True),
        ("/redfish/v1/Systems/1/Memory/proc1dimm1/", "/redfish/v1/Systems/1/Memory/proc1dimm1/",
         True),
        ("/redfish/v1/Systems/1/Memory/proc1dimm2/", "/redfish/v1/Systems/1/Memory/proc1dimm1/",
         False)
    ])
    def test_compare_id(id1, id2, expected_output):
        """
        Test for compare_id()
        :param id1: first id to be compared
        :param id2: second id to be compared
        :param expected_output:
        :return: expected output of the test
        """
        result = PmemHelpers.PmemHelpers.compare_id(id1, id2)
        assert result == expected_output

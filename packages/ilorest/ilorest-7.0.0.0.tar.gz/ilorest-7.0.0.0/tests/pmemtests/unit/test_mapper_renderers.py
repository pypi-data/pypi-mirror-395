"""
This module contains tests for MapperRenderers
"""
from __future__ import absolute_import

import pytest

from .conftest import MapperRenderers


class TestMapperRenderes(object):
    """
    class to test functions in MapperRenderers
    """
    mock_data = [
        {
            "DeviceLocator": "PROC 1 DIMM 1",
            "CapacityMiB": 123456,
            "PersistentRegionSizeLimitMiB": 24680,
            "SizeMiB": "xyz",
            "VolatileRegionSizeLimitMiB": 45678,
        },
        {
            "DeviceLocator": "PROC 2 DIMM 12",
            "CapacityMiB": 987654,
            "PersistentRegionSizeLimitMiB": 13579,
            "SizeMiB": "abc@123",
            "VolatileRegionSizeLimitMiB": 90123,
        }]

    tasks = [
        {
            "Payload": {
                "JsonBody": {
                }
            }
        },
        {
            "Payload": {
                "JsonBody": {
                    "MemoryChunkSizeMiB": 250
                }
            }
        },
        {
            "Payload": {
                "JsonBody": {
                    "Oem": {
                        "Hpe": {
                            "MemoryChunkSizePercentage": 40
                        }
                    }
                }
            }
        },
        {
            "Payload": {
                "JsonBody": {
                    "MemoryChunkSizeMiB": 700,
                    "Oem": {
                        "Hpe": {
                            "MemoryChunkSizePercentage": 25
                        }
                    }
                }
            }
        },
        {
            "Payload": {
                "JsonBody": {
                    "Oem": {
                        "Hpe": {
                            "MemoryChunkSizePercentage": 0
                        }
                    }
                }
            }
        },
        {
            "Payload": {
                "JsonBody": {
                    "MemoryChunkSizeMiB": 0,
                    "Oem": {
                        "Hpe": {
                            "MemoryChunkSizePercentage": 10
                        }
                    }
                }
            }
        }
    ]

    @staticmethod
    @pytest.mark.parametrize("num, expected_output", [
        (0, "0.0 GiB"),
        (20, "0.02 GiB"),
        (400, "0.39 GiB"),
        (1024, "1.0 GiB"),
        (2000, "1.95 GiB"),
        (18499, "18.07 GiB")
    ])
    def test_format_num(num, expected_output):
        """
        Test for format_num()
        :param num: any number
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.format_num(num)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("num, expected_output", [
        (0, {"Units": "GiB", "Value": 0.0}),
        (20, {"Units": "GiB", "Value": 0.02}),
        (400, {"Units": "GiB", "Value": 0.39}),
        (1024, {"Units": "GiB", "Value": 1.0}),
        (2000, {"Units": "GiB", "Value": 1.95}),
        (18499, {"Units": "GiB", "Value": 18.07})
    ])
    def test_format_num_json(num, expected_output):
        """
        Test for format_num_json()
        :param num: any number
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.format_num_json(num)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], "0.0 GiB"),
        ([mock_data[0]], "120.56 GiB"),
        ([mock_data[1]], "964.51 GiB"),
        (mock_data, "1085.07 GiB")
    ])
    def test_calculate_total_capacity(members, expected_output):
        """
        Test for calculate_total_capacity()
        :param members: members for which total capacity needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_capacity(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], {"Units": "GiB", "Value": 0.0}),
        ([mock_data[0]], {"Units": "GiB", "Value": 120.56}),
        ([mock_data[1]], {"Units": "GiB", "Value": 964.51}),
        (mock_data, {"Units": "GiB", "Value": 1085.07})
    ])
    def test_calculate_total_capacity_json(members, expected_output):
        """
        Test for calculate_total_capacity_json()
        :param members: members for which total capacity needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_capacity_json(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], "0.0 GiB"),
        ([mock_data[0]], "44.61 GiB"),
        ([mock_data[1]], "88.01 GiB"),
        (mock_data, "132.62 GiB")
    ])
    def test_calculate_total_volatile(members, expected_output):
        """
        Test for calculate_total_volatile()
        :param members: members for which total volatile size needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_volatile(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], {"Units": "GiB", "Value": 0.0}),
        ([mock_data[0]], {"Units": "GiB", "Value": 44.61}),
        ([mock_data[1]], {"Units": "GiB", "Value": 88.01}),
        (mock_data, {"Units": "GiB", "Value": 132.62})
    ])
    def test_calculate_total_volatile_json(members, expected_output):
        """
        Test for calculate_total_volatile_json()
        :param members: members for which total volatile size needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_volatile_json(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], "0.0 GiB"),
        ([mock_data[0]], "24.1 GiB"),
        ([mock_data[1]], "13.26 GiB"),
        (mock_data, "37.36 GiB")
    ])
    def test_calculate_total_appdirect(members, expected_output):
        """
        Test for calculate_total_appdirect()
        :param members: members for which total appdirect size needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_appdirect(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("members, expected_output", [
        ([], {"Units": "GiB", "Value": 0.0}),
        ([mock_data[0]], {"Units": "GiB", "Value": 24.10}),
        ([mock_data[1]], {"Units": "GiB", "Value": 13.26}),
        (mock_data, {"Units": "GiB", "Value": 37.36})
    ])
    def test_calculate_total_appdirect_json(members, expected_output):
        """
        Test for calculate_total_appdirect_json()
        :param members: members for which total appdirect size needs to be calculated
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_total_appdirect_json(members)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("temp, expected_output", [
        # neither MemoryChunkSizeMiB nor MemoryChunkSizPercentage is present
        ({"Task": tasks[0], "TotalCapacity": 1000}, "1000.0 GiB"),
        # Only MemoryChunkSizeMiB is present
        ({"Task": tasks[1], "TotalCapacity": 1000}, "250.0 GiB"),
        # Only MemoryChunkSizePercentage is present
        ({"Task": tasks[2], "TotalCapacity": 1000}, "400.0 GiB"),
        # Both MemoryChunkSizeMiB and MemoryChunkSizePercentage are present
        ({"Task": tasks[3], "TotalCapacity": 1000}, "700.0 GiB"),
        # MemoryChunkSizePercentage is 0
        ({"Task": tasks[4], "TotalCapacity": 1000}, "0.0 GiB"),
        # MemoryChunkSizeMiB is 0
        ({"Task": tasks[4], "TotalCapacity": 1000}, "0.0 GiB")
    ])
    def test_calculate_task_pmem_size(temp, expected_output):
        """
        Test for calculate_task_pmem_size()
        :param temp: dictionary with task and total capacity of the task as keys
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_task_pmem_size(temp)
        assert out == expected_output
    @staticmethod
    @pytest.mark.parametrize("temp, expected_output", [
        # neither MemoryChunkSizeMiB nor MemoryChunkSizPercentage is present
        ({"Task": tasks[0], "TotalCapacity": 1000}, "1000.0 GiB"),
        # Only MemoryChunkSizeMiB is present
        ({"Task": tasks[1], "TotalCapacity": 1000}, "750.0 GiB"),
        # Only MemoryChunkSizePercentage is present
        ({"Task": tasks[2], "TotalCapacity": 1000}, "600.0 GiB"),
        # Both MemoryChunkSizeMiB and MemoryChunkSizePercentage are present
        ({"Task": tasks[3], "TotalCapacity": 1000}, "300.0 GiB"),
        # MemoryChunkSizePercentage is 0
        ({"Task": tasks[4], "TotalCapacity": 1000}, "1000.0 GiB"),
        # MemoryChunkSizeMiB is 0
        ({"Task": tasks[4], "TotalCapacity": 1000}, "1000.0 GiB")
    ])
    def test_calculate_task_volatile_size(temp, expected_output):
        """
        Test for calculate_task_volatile_size()
        :param temp: dictionary with task and total capacity of the task as keys
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.calculate_task_volatile_size(temp)
        assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize("operation, expected_output", [
        ("post", "post"),
        ("POST", "CREATE"),
        ("GET", "GET"),
        ("get", "get")
    ])
    def test_map_operation(operation, expected_output):
        """
        Test for map_operation()
        :param operation: HTTP operation
        :param expected_output: expected output of the test
        """
        renderers = MapperRenderers.MapperRenderers()
        out = renderers.map_operation(operation)
        assert out == expected_output

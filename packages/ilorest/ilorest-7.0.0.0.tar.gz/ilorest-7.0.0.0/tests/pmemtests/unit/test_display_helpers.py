"""Module to test the DisplayHelpers Class"""
from __future__ import absolute_import

import ast
import sys

import pytest

# For cross-compatibility between Python 2 and Python 3
from six import StringIO

from .conftest import DisplayHelpers


class TestDisplayHelpers(object):
    """
    Class to test methods from the DisplayHelpers class
    """
    output_format = DisplayHelpers.OutputFormats

    @staticmethod
    def capture_stdout(func, data, out_format, prop_id=None):
        """
        Function to capture the standard output stream
        """
        old_stdout = sys.stdout
        capturer = StringIO()
        sys.stdout = capturer
        func(data, out_format, prop_id)
        sys.stdout = old_stdout
        output = capturer.getvalue()
        return output

    @pytest.mark.parametrize('table_data, expected_output', [
        # Tests with empty input
        (None, ""),
        ([], ""),
        # Single object test
        (["ItemId:ID1\nProperty1:Value1"], "ItemId Property1 ID1 Value1"),
        # Test to check truncation of string
        (["ItemId:ID1\nProp2:Value of property2\nProp1:Value1"],
         "ItemId Prop2 Prop1 ID1 Value of.. Value1"),
        # Multiple objects test
        (["ItemId:ID1\nProperty1: ", "ItemId:ID2\nProperty1:LongPropertyValue"],
         "ItemId Property1 ID1 ID2 LongProp..")
    ])
    def test_printtable_withwidth(self, table_data, expected_output):
        """
        Test for printtable with a custom specified width
        """
        display_helpers = DisplayHelpers.DisplayHelpers(10)
        out = TestDisplayHelpers.capture_stdout(
            display_helpers.display_data, table_data, self.output_format.table, None)
        assert [str(x) for x in out.split()] == expected_output.split()

    @pytest.mark.parametrize('table_data, expected_output', [
        # Tests with empty input
        (None, ""),
        ([], ""),
        # Single object test
        (["ItemId:ID1\nProperty1:Value1"], "ItemId Property1 ID1 Value1"),
        # Test to check truncation of string
        (["ItemId:ID1\nProp2:Value of property2\nProp1:Value1"],
         "ItemId Prop2 Prop1 ID1 Value of property2 Value1"),
        # Converting redfish property to friendly name test
        (["Property2:Value2\nFWVersion:2.1"], " Property2 FWVersion Value2 2.1"),
        # Multiple objects test
        (["ItemId:ID1\nProperty1: ", "ItemId:ID2\nProperty1:LongPropertyValue"],
         "ItemId Property1 ID1 ID2 LongPropertyValue")
    ])
    def test_printtable(self, table_data, expected_output):
        """
        Test for printtable with the default width
        """
        display_helpers = DisplayHelpers.DisplayHelpers()
        out = TestDisplayHelpers.capture_stdout(
            display_helpers.display_data, table_data, self.output_format.table, None)
        assert out.split() == expected_output.split()

    @pytest.mark.parametrize('table_data, expected_output', [
        # Tests with empty input
        (None, ""),
        ([], ""),
        # Single object test
        (["ItemId:ID1\nProperty1:Value1"],
         "--- 1 ---\nItemId: ID1\nProperty1: Value1"),
        # Converting redfish property to friendly name test
        (["FWVersion:2.1\nItemId:ID1"], "--- 1 ---\nFWVersion: 2.1\nItemId: ID1"),
        # Multiple objects test
        (["ItemId:ID1\nProperty1:", "ItemId:ID2\nProperty1:Value1"],
         "--- 1 ---\nItemId: ID1\nProperty1: \n\n--- 2 ---\nItemId: ID2\nProperty1: Value1")
    ])
    def test_printlist(self, table_data, expected_output):
        """
        Test for the printlist function that produces output in list form
        """
        display_helpers = DisplayHelpers.DisplayHelpers()
        out = TestDisplayHelpers.capture_stdout(
            display_helpers.display_data, table_data, self.output_format.list, None)
        assert out.strip() == expected_output.strip()

    @pytest.mark.parametrize('table_data, expected_output', [
        # Tests with empty input
        (None, ""),
        ([], ""),
        # Single object test
        (["ItemId:ID1\nProperty1:Value1"],
         "--- ItemId: ID1 ---\nProperty1: Value1"),
        # Converting redfish property to friendly name test
        (["ItemId:ID1\nFWVersion:2.1"], "--- ItemId: ID1 ---\nFWVersion: 2.1"),
        # Multiple objects test
        (["ItemId:ID1\nProperty1:", "ItemId:ID2\nProperty1:Value1"],
         "--- ItemId: ID1 ---\nProperty1: \n\n--- ItemId: ID2 ---\nProperty1: Value1")
    ])
    def test_printlist_withid(self, table_data, expected_output):
        """
        Test for the printlist function that produces output in list form with custom ID
        """
        display_helpers = DisplayHelpers.DisplayHelpers()
        out = TestDisplayHelpers.capture_stdout(
            display_helpers.display_data, table_data, self.output_format.list, "ItemId")
        assert out.strip() == expected_output.strip()

    @pytest.mark.parametrize('table_data, expected_output', [
        # Tests with empty input
        (None, ""),
        ([], ""),
        # Single object test
        ([{"ItemId": "ID1", "Property1": "Value1"}],
         [{"ItemId": "ID1", "Property1": "Value1"}]),
        # Converting redfish property to friendly name test
        ([{"FWVersion": 2.1, "Property2": "Value2"}],
         [{"Property2": "Value2", "FWVersion": 2.1}]),
        # Multiple objects test
        ([{"ItemId": "ID1", "Property1": ""}, {"ItemId": "ID2", "Property1": "LongPropertyValue"}],
         [{"ItemId": "ID1", "Property1": ""}, {"ItemId": "ID2", "Property1": "LongPropertyValue"}])
    ])
    def test_printjson(self, table_data, expected_output):
        """
        Test for the printjson function that produces output in json form
        """
        display_helpers = DisplayHelpers.DisplayHelpers()
        out = TestDisplayHelpers.capture_stdout(
            display_helpers.display_data, table_data, self.output_format.json, None)
        if expected_output == "":
            assert out == expected_output
        else:
            out = ast.literal_eval("".join(out.split()))
            assert out == expected_output

    @staticmethod
    @pytest.mark.parametrize('string, maxlen, expected_output', [
        ("Banana", 10, "Banana"),
        ("Hot Tamale", 10, "Hot Tamale"),
        ("Antidisestablishmentarianism", 10, "Antidise.."),
        ("hippopotomonstrosesquipedaliophobia", 18, "hippopotomonstro.."),
        (None, 10, "")
    ])
    def test_truncate_lengthy(string, maxlen, expected_output):
        """
        Test for the truncate_lengthy method
        """
        display_helpers = DisplayHelpers.DisplayHelpers()
        out = display_helpers.truncate_lengthy(string, maxlen)
        assert out == expected_output

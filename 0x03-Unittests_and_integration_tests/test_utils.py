#!/usr/bin/env python3
"""Unit test for utils.access_nested_map"""
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    def test_access_nested_map(self):
        """Test normal access to nested map"""
        test_cases = [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
        for nested_map, path, expected in test_cases:
            with self.subTest(nested_map=nested_map, path=path):
                result = access_nested_map(nested_map, path)
                self.assertEqual(result, expected)

    def test_access_nested_map_exception(self):
        """Test exception when key is not found"""
        test_cases = [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
        for nested_map, path in test_cases:
            with self.subTest(nested_map=nested_map, path=path):
                with self.assertRaises(KeyError):
                    access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test get_json function"""

    @patch(
        'utils.requests.get',
        return_value=Mock(json=lambda: {"payload": True})
    )
    def test_get_json(self, mock_get):
        """Test that get_json returns the expected result"""
        url = "http://example.com"
        expected = {"payload": True}
        result = get_json(url)
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(url)

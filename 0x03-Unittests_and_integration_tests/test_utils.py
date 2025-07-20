#!/usr/bin/env python3
"""Unit test module for utils.py"""

import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    def test_access_nested_map(self):
        """Test valid inputs"""
        nested_map = {"a": {"b": {"c": 42}}}
        self.assertEqual(access_nested_map(nested_map, ("a",)), {"b": {"c": 42}})
        self.assertEqual(access_nested_map(nested_map, ("a", "b")), {"c": 42})
        self.assertEqual(access_nested_map(nested_map, ("a", "b", "c")), 42)

    def test_access_nested_map_exception(self):
        """Test exception when key is missing"""
        with self.assertRaises(KeyError):
            access_nested_map({}, ("a",))
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ("a", "b"))


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test get_json with mocked requests.get"""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)
            mock_get.reset_mock()


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        """Test that memoized method calls underlying method once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mocked.assert_called_once()


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Unit tests for utils module.
"""
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function."""

    def test_access_nested_map(self):
        """Test standard access_nested_map cases."""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a",)), {"b": 2})
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)

    def test_access_nested_map_exception(self):
        """Test that access_nested_map raises KeyError when path is invalid."""
        with self.assertRaises(KeyError) as ctx1:
            access_nested_map({}, ("a",))
        self.assertEqual(str(ctx1.exception), "'a'")

        with self.assertRaises(KeyError) as ctx2:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(ctx2.exception), "'b'")


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function."""

    def test_get_json(self):
        """Test that get_json returns expected payload and calls requests.get."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
        for test_url, test_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = test_payload

            with patch("utils.requests.get", return_value=mock_response) as mock_get:
                result = get_json(test_url)
                mock_get.assert_called_once_with(test_url)
                self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result after the first call."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            instance = TestClass()
            self.assertEqual(instance.a_property, 42)
            self.assertEqual(instance.a_property, 42)
            mock_method.assert_called_once()

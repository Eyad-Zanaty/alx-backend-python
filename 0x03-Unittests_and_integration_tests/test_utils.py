#!/usr/bin/env python3
"""
Unit tests for utils module.
"""
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result after the first call."""

        class TestClass:
            """Test class for memoization."""

            def a_method(self):
                """Method that returns a constant value."""
                return 42

            @memoize
            def a_property(self):
                """Property that calls a_method and is memoized."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            instance = TestClass()

            result1 = instance.a_property
            result2 = instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

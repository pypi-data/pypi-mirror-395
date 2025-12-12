"""
Tests for emotional_styles.py
"""

import unittest
import re
from pyelling.emotional_styles import SARCASTICALLY, DRAMATICALLY, MOCK


class TestEmotionalStyles(unittest.TestCase):
    def test_sarcastically(self):
        # Test basic functionality
        result = SARCASTICALLY("hello")
        self.assertEqual(result, "hElLo")

        # Test with longer string
        result = SARCASTICALLY("hello world")
        self.assertEqual(result, "hElLo wOrLd")

        # Test with list of strings
        results = SARCASTICALLY(["hello", "world"])
        self.assertEqual(results, ["hElLo", "wOrLd"])

        # Test with empty string
        self.assertEqual(SARCASTICALLY(""), "")

    def test_dramatically(self):
        # Basic test - specific output hard to test due to randomness
        result = DRAMATICALLY("hello")
        self.assertTrue(isinstance(result, str))
        self.assertTrue(len(result) >= 5)  # At least as long as original

        # Test with list
        results = DRAMATICALLY(["hello", "world"])
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(r, str) for r in results))

        # Test with empty string
        self.assertEqual(DRAMATICALLY(""), "")

    def test_mock(self):
        # Test that result has same length as input
        result = MOCK("hello world")
        self.assertEqual(len(result), len("hello world"))

        # Test that case is mixed (at least one upper and one lower)
        self.assertTrue(any(c.isupper() for c in result))
        self.assertTrue(any(c.islower() for c in result))

        # Test with list
        results = MOCK(["hello", "world"])
        self.assertEqual(len(results), 2)

        # Test with empty string
        self.assertEqual(MOCK(""), "")


if __name__ == "__main__":
    unittest.main()
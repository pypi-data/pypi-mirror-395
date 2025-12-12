"""
Tests for internet_effects.py
"""

import unittest
from pyelling.internet_effects import CLAP


class TestInternetEffects(unittest.TestCase):
    def test_clap(self):
        # Test basic clap functionality
        self.assertEqual(CLAP("hello world"), "hello 👏 world")
        self.assertEqual(CLAP("one two three"), "one 👏 two 👏 three")

        # Test with custom emoji
        self.assertEqual(CLAP("hello world", emoji="🔥"), "hello 🔥 world")

        # Test with single word
        self.assertEqual(CLAP("hello"), "hello")

        # Test with empty string
        self.assertEqual(CLAP(""), "")

        # Test with list of strings
        self.assertEqual(CLAP(["hello", "world"]), ["hello", "world"])
        self.assertEqual(
            CLAP(["hello world", "test phrase"]),
            ["hello 👏 world", "test 👏 phrase"]
        )


if __name__ == "__main__":
    unittest.main()
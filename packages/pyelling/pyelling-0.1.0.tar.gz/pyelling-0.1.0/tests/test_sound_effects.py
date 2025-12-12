"""
Tests for sound_effects.py
"""

import unittest
import re
from pyelling.sound_effects import ECHO, STUTTER, VOID_SHOUT


class TestSoundEffects(unittest.TestCase):
    def test_echo(self):
        # Test echo with default settings
        result = ECHO("hello")
        # ECHO now appends to the last word, doesn't necessarily start with the input
        self.assertIn("hello", result)
        self.assertTrue(len(result.split()) > 1)  # Should have multiple words

        # Test echo with fade parameter
        result = ECHO("hello", fade=2)
        parts = result.split()
        self.assertEqual(len(parts), 3)  # Original + 2 echos
        self.assertEqual(parts[0], "hello")

        # Test with multi-word input
        result = ECHO("hello world")
        self.assertTrue(result.startswith("hello world"))

        # Test with list of strings
        results = ECHO(["hello", "world"])
        self.assertEqual(len(results), 2)

        # Test with empty string
        self.assertEqual(ECHO(""), "")

    def test_stutter(self):
        # Test basic stutter functionality
        result = STUTTER("hello")
        self.assertTrue(result.startswith("h-h-hello"))

        # Test with intensity parameter
        result = STUTTER("hello", intensity=1)
        self.assertEqual(result, "h-hello")

        # Test with multi-word input
        result = STUTTER("hello world")
        self.assertTrue("h-h-hello" in result)
        self.assertTrue("w-w-world" in result)

        # Test with list of strings
        results = STUTTER(["hello", "world"])
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].startswith("h-h-hello"))

        # Test with empty string
        self.assertEqual(STUTTER(""), "")

    def test_void_shout(self):
        # Test basic functionality
        result = VOID_SHOUT("hello")
        self.assertEqual(result, "H E L L O")

        # Test with multi-word input
        result = VOID_SHOUT("hello world")
        self.assertEqual(result, "H E L L O   W O R L D")

        # Test with list of strings
        results = VOID_SHOUT(["hello", "world"])
        self.assertEqual(results, ["H E L L O", "W O R L D"])

        # Test with empty string
        self.assertEqual(VOID_SHOUT(""), "")


if __name__ == "__main__":
    unittest.main()
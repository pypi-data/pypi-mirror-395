"""
Tests for text_volume.py
"""

import unittest
from pyelling.text_volume import YELL, WHISPER, INDOOR_VOICE, IS_YELLING


class TestTextVolume(unittest.TestCase):
    def test_yell(self):
        self.assertEqual(YELL("hello"), "HELLO")
        self.assertEqual(YELL("Hello World"), "HELLO WORLD")
        self.assertEqual(YELL(["hello", "world"]), ["HELLO", "WORLD"])
        self.assertEqual(YELL(""), "")

    def test_whisper(self):
        self.assertEqual(WHISPER("HELLO"), "hello")
        self.assertEqual(WHISPER("Hello World"), "hello world")
        self.assertEqual(WHISPER(["HELLO", "WORLD"]), ["hello", "world"])
        self.assertEqual(WHISPER(""), "")

    def test_indoor_voice(self):
        self.assertEqual(INDOOR_VOICE("hello"), "Hello")
        self.assertEqual(INDOOR_VOICE("HELLO WORLD"), "Hello World")
        self.assertEqual(INDOOR_VOICE(["hello", "world"]), ["Hello", "World"])
        self.assertEqual(INDOOR_VOICE(""), "")

    def test_is_yelling(self):
        self.assertTrue(IS_YELLING("HELLO"))
        self.assertFalse(IS_YELLING("Hello"))
        self.assertFalse(IS_YELLING("hello"))
        self.assertTrue(IS_YELLING("123"))  # No letters, considered uppercase
        self.assertEqual(IS_YELLING(["HELLO", "Hello"]), [True, False])


if __name__ == "__main__":
    unittest.main()
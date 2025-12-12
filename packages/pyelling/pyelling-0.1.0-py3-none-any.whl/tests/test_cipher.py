"""
Tests for cipher.py
"""

import unittest
from pyelling.cipher import SCREAM_CIPHER


class TestCipher(unittest.TestCase):
    def test_scream_cipher_encode(self):
        # Test basic encoding
        self.assertEqual(SCREAM_CIPHER("ABC"), "AȦÀ")
        self.assertEqual(SCREAM_CIPHER("HELLO"), "ÅÂǍǍḀ")
        self.assertEqual(SCREAM_CIPHER("hello"), "ÅÂǍǍḀ")  # Case insensitive encoding

        # Test with non-letter characters
        self.assertEqual(SCREAM_CIPHER("A B C"), "A Ȧ À")
        self.assertEqual(SCREAM_CIPHER("123"), "123")
        self.assertEqual(SCREAM_CIPHER("A-Z"), "A-Ẵ")

        # Test with list of strings
        self.assertEqual(SCREAM_CIPHER(["ABC", "XYZ"]), ["AȦÀ", "ẰẲẴ"])

        # Test with empty string
        self.assertEqual(SCREAM_CIPHER(""), "")

    def test_scream_cipher_decode(self):
        # Test basic decoding
        self.assertEqual(SCREAM_CIPHER("AȦÀ", decode=True), "ABC")
        self.assertEqual(SCREAM_CIPHER("ÅÂǍǍḀ", decode=True), "HELLO")

        # Test with non-cipher characters
        self.assertEqual(SCREAM_CIPHER("A Ȧ À", decode=True), "A B C")
        self.assertEqual(SCREAM_CIPHER("123", decode=True), "123")

        # Test with list of strings
        self.assertEqual(
            SCREAM_CIPHER(["AȦÀ", "ẰẲẴ"], decode=True),
            ["ABC", "XYZ"]
        )

        # Test with empty string
        self.assertEqual(SCREAM_CIPHER("", decode=True), "")

    def test_roundtrip(self):
        # Test encode-decode roundtrip
        messages = [
            "Hello World",
            "PYELLING IS AWESOME",
            "123 ABC",
            "Special $#@ Characters!",
            "Mixed CASE text"
        ]

        for message in messages:
            encoded = SCREAM_CIPHER(message)
            decoded = SCREAM_CIPHER(encoded, decode=True)
            self.assertEqual(decoded, message.upper())  # Note: decoded is always uppercase


if __name__ == "__main__":
    unittest.main()
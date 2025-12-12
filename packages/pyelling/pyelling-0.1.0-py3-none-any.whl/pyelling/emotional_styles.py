"""
FUNCTIONS FOR ADDING EMOTIONAL STYLES TO TEXT.
"""

from typing import Union, List
import random


def SARCASTICALLY(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    ADD SARCASTIC TONE TO TEXT BY ALTERNATING CASE.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        TEXT WITH ALTERNATING CASE FOR A SARCASTIC TONE
    """
    def _SARCASTIFY(s: str) -> str:
        result = ""
        for i, char in enumerate(s):
            if i % 2 == 0:
                result += char.lower()
            else:
                result += char.upper()
        return result

    if isinstance(text, list):
        return [_SARCASTIFY(t) for t in text]
    return _SARCASTIFY(text)


def DRAMATICALLY(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    ADD... DRAMATIC... PAUSES... TO TEXT!

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        TEXT WITH DRAMATIC PAUSES AND EMPHASIS
    """
    def _DRAMATIZE(s: str) -> str:
        if not s:
            return s

        words = s.split()
        if len(words) <= 1:
            return s.upper() + "!"

        # Add ellipsis between some words and uppercase a random word
        emphasis_idx = random.randint(0, len(words) - 1)
        result = []

        for i, word in enumerate(words):
            if i == emphasis_idx:
                result.append(word.upper() + "!")
            elif random.random() < 0.3 and i > 0:  # 30% CHANCE OF DRAMATIC PAUSE
                result.append("...")
                result.append(word)
            else:
                result.append(word)

        return " ".join(result)

    if isinstance(text, list):
        return [_DRAMATIZE(t) for t in text]
    return _DRAMATIZE(text)


def MOCK(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    MOCK TEXT BY RANDOMLY ALTERNATING CASE.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        TEXT WITH RANDOMLY ALTERNATING CASE FOR A MOCKING TONE
    """
    def _MOCKIFY(s: str) -> str:
        result = ""
        for char in s:
            if random.random() < 0.5:
                result += char.upper()
            else:
                result += char.lower()
        return result

    if isinstance(text, list):
        return [_MOCKIFY(t) for t in text]
    return _MOCKIFY(text)
"""
FUNCTIONS FOR ADDING SOUND EFFECTS TO TEXT.
"""

from typing import Union, List
import re


def ECHO(text: Union[str, List[str]], fade: int = 3) -> Union[str, List[str]]:
    """
    CREATE AN ECHO EFFECT WITH TEXT, REPEATING AND FADING.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM
        FADE: NUMBER OF ECHO REPETITIONS, DEFAULTS TO 3

    RETURNS:
        TEXT WITH ECHO EFFECT
    """
    def _ADD_ECHO(s: str) -> str:
        if not s:
            return s

        words = s.split()
        if len(words) <= 1:
            result = [s]  # Start with the original word
            result.extend(_ECHO_WORD(s, fade))
            return " ".join(result)

        last_word = words[-1]
        base = " ".join(words)
        echo_parts = _ECHO_WORD(last_word, fade)

        return f"{base} {' '.join(echo_parts)}"

    def _ECHO_WORD(word: str, times: int) -> list:
        result = []
        for i in range(1, times + 1):
            # Gradually reduce letters based on echo count
            reduced = word[0:max(1, len(word) - i)]
            result.append(reduced.lower())
        return result

    if isinstance(text, list):
        return [_ADD_ECHO(t) for t in text]
    return _ADD_ECHO(text)


def STUTTER(text: Union[str, List[str]], intensity: int = 2) -> Union[str, List[str]]:
    """
    A-A-ADD ST-STUTTER EFFECT TO T-TEXT.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM
        INTENSITY: LEVEL OF STUTTERING EFFECT, DEFAULTS TO 2

    RETURNS:
        TEXT WITH STUTTER EFFECT
    """
    def _ADD_STUTTER(s: str) -> str:
        if not s or len(s) < 2:
            return s

        words = s.split()
        result = []

        for word in words:
            if len(word) <= 1 or len(word) > 20:  # SKIP VERY SHORT OR LONG WORDS
                result.append(word)
                continue

            # ADD STUTTER TO WORD
            first_letter = word[0]
            stutter_part = f"{first_letter}-" * intensity
            result.append(f"{stutter_part}{word}")

        return " ".join(result)

    if isinstance(text, list):
        return [_ADD_STUTTER(t) for t in text]
    return _ADD_STUTTER(text)


def VOID_SHOUT(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    CONVERT TEXT TO UPPERCASE AND ADD EXTRA SPACE BETWEEN EACH LETTER.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        TEXT WITH VOID SHOUTING EFFECT
    """
    def _VOID_SHOUT(s: str) -> str:
        upper = s.upper()
        # ADD SPACES BETWEEN EACH CHARACTER
        return " ".join(upper)

    if isinstance(text, list):
        return [_VOID_SHOUT(t) for t in text]
    return _VOID_SHOUT(text)
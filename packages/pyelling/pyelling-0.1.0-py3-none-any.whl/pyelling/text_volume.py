"""
FUNCTIONS FOR TEXT VOLUME TRANSFORMATIONS.
"""

from typing import Union, List


def YELL(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    CONVERT TEXT TO UPPERCASE, SIMULATING YELLING.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        THE UPPERCASE VERSION OF THE INPUT TEXT
    """
    if isinstance(text, list):
        return [t.upper() for t in text]
    return text.upper()


def WHISPER(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    CONVERT TEXT TO LOWERCASE, SIMULATING WHISPERING.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        THE LOWERCASE VERSION OF THE INPUT TEXT
    """
    if isinstance(text, list):
        return [t.lower() for t in text]
    return text.lower()


def INDOOR_VOICE(text: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    CONVERT TEXT TO TITLE CASE, FOR A MORE MODERATE TONE.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM

    RETURNS:
        THE TITLE CASE VERSION OF THE INPUT TEXT
    """
    if isinstance(text, list):
        return [t.title() for t in text]
    return text.title()


def IS_YELLING(text: Union[str, List[str]]) -> Union[bool, List[bool]]:
    """
    CHECK IF TEXT IS IN ALL UPPERCASE.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO CHECK

    RETURNS:
        TRUE IF TEXT IS UPPERCASE, FALSE OTHERWISE
    """
    def _IS_YELLING(s: str) -> bool:
        # FOR STRINGS WITH NO LETTERS, LIKE "123", TREAT THEM AS UPPERCASE
        if not any(c.isalpha() for c in s):
            return True
        return s.isupper()

    if isinstance(text, list):
        return [_IS_YELLING(t) for t in text]
    return _IS_YELLING(text)
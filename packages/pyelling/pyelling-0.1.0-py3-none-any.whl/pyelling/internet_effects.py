"""
FUNCTIONS FOR ADDING INTERNET CULTURE EFFECTS TO TEXT.
"""

from typing import Union, List


def CLAP(text: Union[str, List[str]], emoji: str = "👏") -> Union[str, List[str]]:
    """
    INSERT 👏 CLAP 👏 EMOJIS 👏 BETWEEN 👏 WORDS.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM
        EMOJI: EMOJI TO INSERT BETWEEN WORDS, DEFAULTS TO 👏

    RETURNS:
        TEXT WITH EMOJIS BETWEEN WORDS
    """
    def _ADD_CLAPS(s: str) -> str:
        words = s.split()
        if len(words) <= 1:
            return s
        return f" {emoji} ".join(words)

    if isinstance(text, list):
        return [_ADD_CLAPS(t) for t in text]
    return _ADD_CLAPS(text)
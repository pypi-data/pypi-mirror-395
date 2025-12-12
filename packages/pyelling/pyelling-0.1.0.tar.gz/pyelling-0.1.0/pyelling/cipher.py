"""
FUNCTIONS FOR TEXT CIPHER TRANSFORMATIONS.
"""

from typing import Union, List


def SCREAM_CIPHER(text: Union[str, List[str]], decode: bool = False) -> Union[str, List[str]]:
    """
    TRANSFORM TEXT USING THE SCREAM CIPHER, REPLACING LETTERS WITH DIACRITICAL 'A' CHARACTERS.

    ARGS:
        TEXT: INPUT TEXT OR LIST OF STRINGS TO TRANSFORM
        DECODE: IF TRUE, DECODE THE TEXT INSTEAD OF ENCODING IT

    RETURNS:
        ENCODED OR DECODED TEXT
    """
    scream_alphabet = {
        'A': 'A',          # A - PLAIN
        'B': '\u0226',     # B - Ȧ (DOT ABOVE)
        'C': '\u00C0',     # C - À (GRAVE)
        'D': '\u00C1',     # D - Á (ACUTE)
        'E': '\u00C2',     # E - Â (CIRCUMFLEX)
        'F': '\u00C3',     # F - Ã (TILDE)
        'G': '\u00C4',     # G - Ä (DIAERESIS)
        'H': '\u00C5',     # H - Å (RING ABOVE)
        'I': '\u0100',     # I - Ā (MACRON)
        'J': '\u0102',     # J - Ă (BREVE)
        'K': '\u0104',     # K - Ą (OGONEK)
        'L': '\u01CD',     # L - Ǎ (CARON)
        'M': '\u0200',     # M - Ȁ (DOUBLE GRAVE)
        'N': '\u0202',     # N - Ȃ (INVERTED BREVE)
        'O': '\u1E00',     # O - Ḁ (RING BELOW)
        'P': '\u1EA0',     # P - Ạ (DOT BELOW)
        'Q': '\u1EA2',     # Q - Ả (HOOK ABOVE)
        'R': '\u1EA4',     # R - Ấ (CIRCUMFLEX ACUTE)
        'S': '\u1EA6',     # S - Ầ (CIRCUMFLEX GRAVE)
        'T': '\u1EA8',     # T - Ẩ (CIRCUMFLEX HOOK)
        'U': '\u1EAA',     # U - Ẫ (CIRCUMFLEX TILDE)
        'V': '\u1EAC',     # V - Ậ (CIRCUMFLEX DOT BELOW)
        'W': '\u1EAE',     # W - Ắ (BREVE ACUTE)
        'X': '\u1EB0',     # X - Ằ (BREVE GRAVE)
        'Y': '\u1EB2',     # Y - Ẳ (BREVE HOOK)
        'Z': '\u1EB4'      # Z - Ẵ (BREVE TILDE)
    }

    def PROCESS_STRING(s: str) -> str:
        if decode:
            # CREATE REVERSE MAPPING FOR DECODING
            decode_map = {v: k for k, v in scream_alphabet.items()}
            result = []
            for ch in s:
                if ch in decode_map:
                    result.append(decode_map[ch])
                else:
                    result.append(ch)
            return "".join(result)
        else:
            # ENCODING - CONVERT TO UPPERCASE FIRST
            s = s.upper()
            result = []
            for ch in s:
                if ch in scream_alphabet:
                    result.append(scream_alphabet[ch])
                else:
                    result.append(ch)
            return "".join(result)

    if isinstance(text, list):
        return [PROCESS_STRING(s) for s in text]
    return PROCESS_STRING(text)
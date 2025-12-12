# PYELLING

A Python package for TEXT TRANSFORMATION! This is a Python port of the [YELLING](https://github.com/hadley/YELLING) R package by Hadley Wickham.

## Installation

```bash
pip install pyelling
```

## Usage

```python
from pyelling import YELL, WHISPER, CLAP, MOCK

# Basic usage
YELL("hello world")  # Returns: "HELLO WORLD"
WHISPER("QUIET PLEASE")  # Returns: "quiet please"
CLAP("make some noise")  # Returns: "make 👏 some 👏 noise"
MOCK("I totally agree")  # Returns something like: "i ToTaLlY aGrEe"

# You can also use it with lists of strings
YELL(["hello", "world"])  # Returns: ["HELLO", "WORLD"]
```

## Available Functions

### Text Volume
- `YELL(text)`: CONVERT TEXT TO UPPERCASE
- `WHISPER(text)`: convert text to lowercase
- `INDOOR_VOICE(text)`: Convert Text To Title Case
- `IS_YELLING(text)`: Check if text is ALL UPPERCASE

### Emotional Styles
- `SARCASTICALLY(text)`: aDd SaRcAsTiC tExT aLtErNaTiOn
- `DRAMATICALLY(text)`: Add... DRAMATIC... pauses!
- `MOCK(text)`: RaNdOmLy AlTeRnAtE cAsE fOr MoCkInG

### Internet Effects
- `CLAP(text, emoji="👏")`: Add 👏 clap 👏 emojis 👏 between 👏 words

### Sound Effects
- `ECHO(text, fade=3)`: Add echo effect to text (text text tex te t)
- `STUTTER(text, intensity=2)`: A-a-add st-stutter to words
- `VOID_SHOUT(text)`: S P A C E  O U T  T E X T

### Cipher
- `SCREAM_CIPHER(text, decode=False)`: Encode text using special 'A' characters with diacritical marks

## License

MIT
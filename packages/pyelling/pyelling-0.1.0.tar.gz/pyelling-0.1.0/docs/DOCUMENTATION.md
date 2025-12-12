# PYELLING Package Documentation

PYELLING is a Python package for creative text transformations, inspired by the [YELLING](https://github.com/hadley/YELLING) R package by Hadley Wickham.

## Installation

```bash
pip install pyelling
```

## Features

PYELLING provides a collection of functions for transforming text in creative ways, organized into different categories:

### Text Volume Functions

#### `YELL(text)`
Converts all characters to uppercase.

```python
from pyelling import YELL

YELL("hello world")  # Returns: "HELLO WORLD"
YELL(["hello", "world"])  # Returns: ["HELLO", "WORLD"]
```

#### `WHISPER(text)`
Converts all characters to lowercase.

```python
from pyelling import WHISPER

WHISPER("HELLO WORLD")  # Returns: "hello world"
WHISPER(["HELLO", "WORLD"])  # Returns: ["hello", "world"]
```

#### `INDOOR_VOICE(text)`
Converts text to title case (first letter of each word capitalized).

```python
from pyelling import INDOOR_VOICE

INDOOR_VOICE("hello world")  # Returns: "Hello World"
INDOOR_VOICE(["hello", "world"])  # Returns: ["Hello", "World"]
```

#### `IS_YELLING(text)`
Checks if the text is all uppercase.

```python
from pyelling import IS_YELLING

IS_YELLING("HELLO")  # Returns: True
IS_YELLING("Hello")  # Returns: False
IS_YELLING(["HELLO", "world"])  # Returns: [True, False]
```

### Emotional Style Functions

#### `SARCASTICALLY(text)`
Alternates character case to create a sarcastic tone.

```python
from pyelling import SARCASTICALLY

SARCASTICALLY("hello world")  # Returns: "hElLo WoRlD"
```

#### `DRAMATICALLY(text)`
Adds dramatic pauses and emphasis to text.

```python
from pyelling import DRAMATICALLY

# Output varies due to randomness
DRAMATICALLY("hello world")  # Might return: "hello... WORLD!"
```

#### `MOCK(text)`
Randomly alternates case for a mocking tone.

```python
from pyelling import MOCK

# Output varies due to randomness
MOCK("I agree")  # Might return: "i aGreE"
```

### Internet Effects

#### `CLAP(text, emoji="👏")`
Inserts clap emojis between words.

```python
from pyelling import CLAP

CLAP("make some noise")  # Returns: "make 👏 some 👏 noise"
CLAP("hello world", emoji="🔥")  # Returns: "hello 🔥 world"
```

### Sound Effects

#### `ECHO(text, fade=3)`
Creates an echo effect, repeating and fading the last word.

```python
from pyelling import ECHO

ECHO("hello world")  # Returns: "hello world world worl wor"
ECHO("hello", fade=2)  # Returns: "hello hell hel"
```

#### `STUTTER(text, intensity=2)`
Adds a stutter effect to the beginning of words.

```python
from pyelling import STUTTER

STUTTER("hello world")  # Returns: "h-h-hello w-w-world"
STUTTER("hello", intensity=1)  # Returns: "h-hello"
```

#### `VOID_SHOUT(text)`
Adds spaces between each character, as if shouting into the void.

```python
from pyelling import VOID_SHOUT

VOID_SHOUT("hello")  # Returns: "H E L L O"
```

### Cipher

#### `SCREAM_CIPHER(text, decode=False)`
Encodes text by replacing each letter with a diacritical variant of 'A'.

```python
from pyelling import SCREAM_CIPHER

# Encoding
SCREAM_CIPHER("HELLO")  # Returns: "ÅÂǍǍḀ"

# Decoding
SCREAM_CIPHER("ÅÂǍǍḀ", decode=True)  # Returns: "HELLO"

# It preserves non-letter characters
SCREAM_CIPHER("HELLO WORLD!")  # Returns: "ÅÂǍǍḀ ẮḀẤǍD!"

# Works with lists too
SCREAM_CIPHER(["ABC", "XYZ"])  # Returns: ["AȦÀ", "ẰẲẴ"]
```

## Input Types

All functions in PYELLING accept either a string or a list of strings:

```python
from pyelling import YELL

# Single string input
YELL("hello")  # Returns: "HELLO"

# List of strings input
YELL(["hello", "world"])  # Returns: ["HELLO", "WORLD"]
```

## Examples

### Combining Functions

You can combine multiple PYELLING functions for more complex transformations:

```python
from pyelling import YELL, CLAP, VOID_SHOUT

# Convert to uppercase, then add claps
CLAP(YELL("important message"))  # Returns: "IMPORTANT 👏 MESSAGE"

# Space out characters and add claps
CLAP(VOID_SHOUT("spooky"))  # Returns: "S 👏 P 👏 O 👏 O 👏 K 👏 Y"
```

### Processing Multiple Strings

```python
from pyelling import YELL, WHISPER, INDOOR_VOICE

phrases = ["hello world", "goodbye world", "see you later"]

# Process all phrases at once
yelled = YELL(phrases)  # ["HELLO WORLD", "GOODBYE WORLD", "SEE YOU LATER"]
whispered = WHISPER(phrases)  # ["hello world", "goodbye world", "see you later"]
indoor = INDOOR_VOICE(phrases)  # ["Hello World", "Goodbye World", "See You Later"]
```

## License

MIT
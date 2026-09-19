"""
Helper utilities for handling Arabic-specific text quirks in data.
"""

import re

# Arabic-Indic digit to Latin digit mapping
ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"
LATIN_DIGITS = "0123456789"
_DIGIT_TRANSLATION = str.maketrans(ARABIC_INDIC_DIGITS, LATIN_DIGITS)

_ARABIC_DIGIT_RE = re.compile(f"[{ARABIC_INDIC_DIGITS}]")
_LATIN_DIGIT_RE = re.compile(r"[0-9]")


def contains_arabic_indic_digits(text: str) -> bool:
    """Return True if the text contains Arabic-Indic digits."""
    return bool(_ARABIC_DIGIT_RE.search(text))


def has_mixed_digits(text: str) -> bool:
    """Return True if the text mixes Arabic-Indic and Latin digits."""
    return bool(_ARABIC_DIGIT_RE.search(text)) and bool(_LATIN_DIGIT_RE.search(text))


def normalize_digits(text: str) -> str:
    """Convert all Arabic-Indic digits in the text to Latin digits."""
    if not isinstance(text, str):
        return text
    return text.translate(_DIGIT_TRANSLATION)


def likely_encoding_issue(raw_bytes: bytes) -> str | None:
    """
    Try to detect whether the file uses a common non-UTF-8 encoding for
    Arabic text (such as Windows-1256), returning the likely encoding name,
    or None if the bytes are valid UTF-8.
    """
    try:
        raw_bytes.decode("utf-8")
        return None
    except UnicodeDecodeError:
        pass

    for encoding in ("windows-1256", "iso-8859-6", "cp720"):
        try:
            raw_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return None


def detect_column_digit_issues(values: list[str]) -> bool:
    """Check a single column's values across rows for mixed digit systems."""
    joined_has_arabic = any(contains_arabic_indic_digits(v) for v in values if isinstance(v, str))
    joined_has_latin = any(_LATIN_DIGIT_RE.search(v) for v in values if isinstance(v, str))
    return joined_has_arabic and joined_has_latin

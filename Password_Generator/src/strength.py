"""
strength.py — Password strength analysis engine.

Analyses a generated (or user-supplied) password against a set of
weighted criteria and returns a structured StrengthReport.

Criteria and scoring
──────────────────────────────────────────
  Length bonus       0 – 40 pts  (logarithmic scale)
  Uppercase chars    0 – 10 pts
  Lowercase chars    0 – 10 pts
  Digit chars        0 – 10 pts
  Symbol chars       0 – 15 pts
  Character variety  0 – 15 pts  (unique char ratio)
──────────────────────────────────────────
  Max total            100 pts

Rating thresholds
  Very Weak   0 – 19
  Weak       20 – 39
  Fair       40 – 59
  Strong     60 – 79
  Very Strong 80+
"""

import math
import string
from dataclasses import dataclass, field
from typing import Literal

# ──────────────────────────────────────────────────────────────
# Types
# ──────────────────────────────────────────────────────────────

StrengthRating = Literal[
    "Very Weak", "Weak", "Fair", "Strong", "Very Strong"
]

RATING_EMOJI: dict[str, str] = {
    "Very Weak":  "🔴",
    "Weak":       "🟠",
    "Fair":       "🟡",
    "Strong":     "🟢",
    "Very Strong":"💎",
}

# ──────────────────────────────────────────────────────────────
# Character sets
# ──────────────────────────────────────────────────────────────

_UPPER   = set(string.ascii_uppercase)
_LOWER   = set(string.ascii_lowercase)
_DIGITS  = set(string.digits)
_SYMBOLS = set(string.punctuation)


# ──────────────────────────────────────────────────────────────
# Report dataclass
# ──────────────────────────────────────────────────────────────


@dataclass
class StrengthReport:
    """
    Full strength analysis of a password.

    Attributes:
        password:        The analysed password string.
        score:           Composite score 0 – 100.
        rating:          Human-readable strength label.
        length:          Total character count.
        upper_count:     Number of uppercase characters.
        lower_count:     Number of lowercase characters.
        digit_count:     Number of digit characters.
        symbol_count:    Number of symbol characters.
        unique_count:    Number of distinct characters.
        suggestions:     List of improvement tips (empty for strong passwords).
    """

    password: str
    score: int
    rating: StrengthRating
    length: int
    upper_count: int
    lower_count: int
    digit_count: int
    symbol_count: int
    unique_count: int
    suggestions: list[str] = field(default_factory=list)

    @property
    def rating_emoji(self) -> str:
        """Coloured emoji that represents the strength rating."""
        return RATING_EMOJI.get(self.rating, "❓")

    @property
    def variety_count(self) -> int:
        """Number of character categories present (0 – 4)."""
        return sum([
            self.upper_count > 0,
            self.lower_count > 0,
            self.digit_count > 0,
            self.symbol_count > 0,
        ])

    def display(self) -> str:
        """
        Return a formatted multi-line summary string.

        Returns:
            Ready-to-print string with all report fields.
        """
        sep = "  " + "─" * 38
        lines = [
            "",
            sep,
            f"  📊  Password Analysis",
            sep,
            f"  🔑  Password     : {self.password}",
            f"  📏  Length       : {self.length} characters",
            sep,
            f"  🔠  Uppercase    : {self.upper_count}",
            f"  🔡  Lowercase    : {self.lower_count}",
            f"  🔢  Digits       : {self.digit_count}",
            f"  🔣  Symbols      : {self.symbol_count}",
            f"  🎲  Unique chars : {self.unique_count}",
            f"  🎨  Categories   : {self.variety_count} / 4",
            sep,
            f"  {self.rating_emoji}  Strength     : {self.rating}  ({self.score}/100)",
            sep,
        ]
        if self.suggestions:
            lines.append("  💡  Suggestions:")
            for tip in self.suggestions:
                lines.append(f"       • {tip}")
            lines.append(sep)
        return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Scoring helpers (pure functions)
# ──────────────────────────────────────────────────────────────


def _length_score(length: int) -> int:
    """
    Map password length to a score in [0, 40] using a log curve.

    Calibration points:
      length  4  →  ~5
      length  8  →  ~15
      length 12  →  ~23
      length 16  →  ~30
      length 32  →  ~40
    """
    if length <= 0:
        return 0
    raw = math.log(length + 1) / math.log(33) * 40
    return min(int(raw), 40)


def _char_score(count: int, max_pts: int) -> int:
    """
    Give partial credit for character-category presence.

    Args:
        count:   How many characters of this category are present.
        max_pts: Maximum points available for this category.

    Returns:
        Integer score in [0, max_pts].
    """
    if count == 0:
        return 0
    if count == 1:
        return max_pts // 2
    return max_pts


def _variety_score(unique: int, total: int) -> int:
    """
    Reward uniqueness (low repetition) in [0, 15].

    Args:
        unique: Number of distinct characters.
        total:  Total password length.

    Returns:
        Integer score in [0, 15].
    """
    if total == 0:
        return 0
    ratio = unique / total
    return min(int(ratio * 15), 15)


def _rating_from_score(score: int) -> StrengthRating:
    """
    Map a numeric score to a StrengthRating label.

    Args:
        score: Composite score in [0, 100].

    Returns:
        StrengthRating literal.
    """
    if score >= 80:
        return "Very Strong"
    if score >= 60:
        return "Strong"
    if score >= 40:
        return "Fair"
    if score >= 20:
        return "Weak"
    return "Very Weak"


def _build_suggestions(
    length: int,
    upper: int,
    lower: int,
    digits: int,
    symbols: int,
    score: int,
) -> list[str]:
    """
    Generate actionable improvement suggestions.

    Args:
        length:  Password length.
        upper:   Uppercase count.
        lower:   Lowercase count.
        digits:  Digit count.
        symbols: Symbol count.
        score:   Current composite score.

    Returns:
        List of suggestion strings (may be empty for strong passwords).
    """
    tips: list[str] = []
    if length < 12:
        tips.append("Use at least 12 characters for better security.")
    if upper == 0:
        tips.append("Add uppercase letters (A–Z).")
    if lower == 0:
        tips.append("Add lowercase letters (a–z).")
    if digits == 0:
        tips.append("Include digits (0–9).")
    if symbols == 0:
        tips.append("Include special symbols (!, @, #, …).")
    if score >= 80:
        tips = []  # No suggestions for very strong passwords
    return tips


# ──────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────


def analyse(password: str) -> StrengthReport:
    """
    Analyse a password and return a full StrengthReport.

    Args:
        password: The password string to analyse.

    Returns:
        A populated StrengthReport instance.
    """
    chars = list(password)
    length       = len(chars)
    upper_count  = sum(1 for c in chars if c in _UPPER)
    lower_count  = sum(1 for c in chars if c in _LOWER)
    digit_count  = sum(1 for c in chars if c in _DIGITS)
    symbol_count = sum(1 for c in chars if c in _SYMBOLS)
    unique_count = len(set(chars))

    score = sum([
        _length_score(length),
        _char_score(upper_count,  10),
        _char_score(lower_count,  10),
        _char_score(digit_count,  10),
        _char_score(symbol_count, 15),
        _variety_score(unique_count, length),
    ])
    score = min(score, 100)

    rating = _rating_from_score(score)
    suggestions = _build_suggestions(
        length, upper_count, lower_count, digit_count, symbol_count, score
    )

    return StrengthReport(
        password=password,
        score=score,
        rating=rating,
        length=length,
        upper_count=upper_count,
        lower_count=lower_count,
        digit_count=digit_count,
        symbol_count=symbol_count,
        unique_count=unique_count,
        suggestions=suggestions,
    )

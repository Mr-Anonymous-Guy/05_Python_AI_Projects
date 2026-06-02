"""
utils.py — Console UI helpers and shared constants.

Handles all terminal I/O, formatting, and cross-platform utilities
so every other module stays free of print() and input() calls.
"""

import os
import sys
from typing import Optional

# ──────────────────────────────────────────────────────────────
# Visual constants
# ──────────────────────────────────────────────────────────────

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║            🔐  PROFESSIONAL PASSWORD GENERATOR        ║
╚══════════════════════════════════════════════════════╝
"""

SEPARATOR = "─" * 54
THIN_SEP  = "·" * 54


# ──────────────────────────────────────────────────────────────
# Console helpers
# ──────────────────────────────────────────────────────────────


def clear_screen() -> None:
    """Clear the terminal in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Print the application banner."""
    print(BANNER)


def print_separator(thin: bool = False) -> None:
    """Print a horizontal divider line."""
    print(THIN_SEP if thin else SEPARATOR)


def print_success(msg: str) -> None:
    """Print a green-prefixed success message."""
    print(f"  ✅  {msg}")


def print_error(msg: str) -> None:
    """Print a red-prefixed error message."""
    print(f"  ⚠️   {msg}")


def print_info(msg: str) -> None:
    """Print a neutral info message."""
    print(f"  ℹ️   {msg}")


# ──────────────────────────────────────────────────────────────
# Input helpers
# ──────────────────────────────────────────────────────────────


def get_input(prompt: str) -> str:
    """
    Read a line of input, stripping surrounding whitespace.

    Args:
        prompt: Message shown before the cursor.

    Returns:
        Cleaned, lower-cased string.

    Raises:
        SystemExit: On EOF or CTRL-C so the app exits gracefully.
    """
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  👋  Goodbye!\n")
        sys.exit(0)


def get_int_input(
    prompt: str,
    min_val: int = 1,
    max_val: int = 10_000,
) -> Optional[int]:
    """
    Prompt the user for an integer within [min_val, max_val].

    Returns None if the input is not a valid integer or out of range,
    so the caller can loop and show an appropriate error message.

    Args:
        prompt:  Display prompt.
        min_val: Inclusive lower bound.
        max_val: Inclusive upper bound.

    Returns:
        Parsed integer, or None on invalid input.
    """
    raw = get_input(prompt)
    try:
        value = int(raw)
    except ValueError:
        return None
    if not (min_val <= value <= max_val):
        return None
    return value


def get_menu_choice(prompt: str, valid: set[str]) -> str:
    """
    Prompt until the user picks one of the allowed options.

    Args:
        prompt: Display prompt string.
        valid:  Set of accepted answer strings (comparison is lower-cased).

    Returns:
        The validated input string (lower-cased).
    """
    while True:
        raw = get_input(prompt).lower()
        if raw in valid:
            return raw
        print_error(f"Please enter one of: {', '.join(sorted(valid))}")


def confirm(prompt: str) -> bool:
    """
    Ask a yes/no question.

    Args:
        prompt: Question text.

    Returns:
        True for 'y', False for 'n'.
    """
    answer = get_menu_choice(f"  {prompt} [y/n]: ", {"y", "n"})
    return answer == "y"

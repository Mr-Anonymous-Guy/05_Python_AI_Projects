"""
utils.py — Utility functions for Rock Paper Scissors.

Handles console UI, input validation, and display helpers.
"""

import os
import sys
from typing import Optional

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

VALID_CHOICES: dict[str, str] = {
    "1": "Rock",
    "2": "Paper",
    "3": "Scissors",
    "r": "Rock",
    "p": "Paper",
    "s": "Scissors",
    "rock": "Rock",
    "paper": "Paper",
    "scissors": "Scissors",
}

CHOICE_EMOJI: dict[str, str] = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️",
}

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║        ✊ 🖐  ✌  ROCK  PAPER  SCISSORS  ✊ 🖐  ✌       ║
╚══════════════════════════════════════════════════════╝
"""

SEPARATOR = "─" * 54


# ──────────────────────────────────────────────────────────────
# Console helpers
# ──────────────────────────────────────────────────────────────


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Print the game banner."""
    print(BANNER)


def print_separator() -> None:
    """Print a horizontal divider line."""
    print(SEPARATOR)


def print_centered(text: str) -> None:
    """Print text centred within the separator width."""
    print(text.center(54))


# ──────────────────────────────────────────────────────────────
# Input helpers
# ──────────────────────────────────────────────────────────────


def get_input(prompt: str) -> str:
    """
    Read a line of input, stripping whitespace.

    Args:
        prompt: The message shown to the user.

    Returns:
        The cleaned input string (lower-cased).
    """
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  👋  Thanks for playing! Goodbye.\n")
        sys.exit(0)


def validate_choice(raw: str) -> Optional[str]:
    """
    Map raw user input to a canonical choice name.

    Args:
        raw: The raw input string.

    Returns:
        "Rock", "Paper", or "Scissors" on success; None otherwise.
    """
    return VALID_CHOICES.get(raw.lower())


def get_valid_choice() -> str:
    """
    Prompt the player until they enter a valid move.

    Returns:
        A validated canonical choice string.
    """
    while True:
        raw = get_input(
            "\n  Your move → [1] Rock  [2] Paper  [3] Scissors : "
        )
        choice = validate_choice(raw)
        if choice:
            return choice
        print("  ⚠️  Invalid input. Please enter 1, 2, 3  (or r / p / s).")


def get_menu_choice(prompt: str, valid: set[str]) -> str:
    """
    Prompt until the user picks one of the allowed options.

    Args:
        prompt: The display prompt string.
        valid:  Set of accepted answer strings (lower-cased).

    Returns:
        The validated input string.
    """
    while True:
        raw = get_input(prompt)
        if raw in valid:
            return raw
        print(f"  ⚠️  Please enter one of: {', '.join(sorted(valid))}")

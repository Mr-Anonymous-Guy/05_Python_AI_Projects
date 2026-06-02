"""
player.py — Player representations for Rock Paper Scissors.

Defines both the human player and the computer (AI) player.
The computer uses Python's ``random`` module to make its move.
"""

import random
from typing import ClassVar


# ──────────────────────────────────────────────────────────────
# Base class
# ──────────────────────────────────────────────────────────────


class Player:
    """Abstract base for any Rock Paper Scissors player."""

    CHOICES: ClassVar[list[str]] = ["Rock", "Paper", "Scissors"]

    def __init__(self, name: str) -> None:
        """
        Initialise the player.

        Args:
            name: Display name for the player.
        """
        self.name: str = name

    def get_choice(self) -> str:
        """Return the player's chosen move. Must be overridden."""
        raise NotImplementedError("Subclasses must implement get_choice()")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"


# ──────────────────────────────────────────────────────────────
# Human player
# ──────────────────────────────────────────────────────────────


class HumanPlayer(Player):
    """A human-controlled player that reads moves from stdin."""

    def __init__(self, name: str = "You") -> None:
        super().__init__(name)

    def get_choice(self) -> str:
        """
        Delegate to the utility input validator.

        The import is kept local to avoid a circular dependency between
        player.py and utils.py.

        Returns:
            A validated move string ("Rock", "Paper", or "Scissors").
        """
        from src.utils import get_valid_choice  # local import — avoids circular dep

        return get_valid_choice()


# ──────────────────────────────────────────────────────────────
# Computer player
# ──────────────────────────────────────────────────────────────


class ComputerPlayer(Player):
    """A computer-controlled player that picks moves at random."""

    def __init__(self, name: str = "Computer") -> None:
        super().__init__(name)

    def get_choice(self) -> str:
        """
        Pick a random move.

        Returns:
            One of "Rock", "Paper", or "Scissors" chosen uniformly at random.
        """
        return random.choice(self.CHOICES)

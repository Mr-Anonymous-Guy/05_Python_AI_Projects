"""
stats.py — Session and cumulative statistics for Rock Paper Scissors.

Tracks wins, losses, and draws both for the current game session
and across the entire runtime lifetime of the process.
"""

from dataclasses import dataclass, field
from typing import Literal

Result = Literal["win", "loss", "draw"]


# ──────────────────────────────────────────────────────────────
# Data class
# ──────────────────────────────────────────────────────────────


@dataclass
class Stats:
    """
    Mutable statistics container.

    Attributes:
        wins:   Number of rounds the human player won.
        losses: Number of rounds the human player lost.
        draws:  Number of rounds that ended in a draw.
    """

    wins: int = field(default=0)
    losses: int = field(default=0)
    draws: int = field(default=0)

    # ── derived properties ──────────────────────────────────

    @property
    def total(self) -> int:
        """Total number of rounds recorded."""
        return self.wins + self.losses + self.draws

    @property
    def win_rate(self) -> float:
        """
        Win-rate as a percentage in the range [0.0, 100.0].

        Returns 0.0 when no rounds have been played yet.
        """
        if self.total == 0:
            return 0.0
        return (self.wins / self.total) * 100

    # ── mutation ────────────────────────────────────────────

    def record(self, result: Result) -> None:
        """
        Increment the appropriate counter.

        Args:
            result: "win", "loss", or "draw".

        Raises:
            ValueError: If result is not one of the three valid literals.
        """
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        elif result == "draw":
            self.draws += 1
        else:
            raise ValueError(f"Unknown result: {result!r}")

    def reset(self) -> None:
        """Reset all counters to zero (used between game sessions)."""
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def merge(self, other: "Stats") -> None:
        """
        Add the counts from *other* into this object (cumulative totals).

        Args:
            other: Another Stats instance whose results will be absorbed.
        """
        self.wins += other.wins
        self.losses += other.losses
        self.draws += other.draws

    # ── display ─────────────────────────────────────────────

    def summary(self, label: str = "Stats") -> str:
        """
        Return a multi-line statistics summary string.

        Args:
            label: Header label printed above the table.

        Returns:
            A formatted string ready to print to the console.
        """
        lines = [
            f"\n  {'─' * 36}",
            f"  📊  {label}",
            f"  {'─' * 36}",
            f"  🎮  Rounds Played : {self.total}",
            f"  ✅  Wins          : {self.wins}",
            f"  ❌  Losses        : {self.losses}",
            f"  🤝  Draws         : {self.draws}",
            f"  📈  Win Rate      : {self.win_rate:.1f}%",
            f"  {'─' * 36}",
        ]
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"Stats(wins={self.wins}, losses={self.losses}, "
            f"draws={self.draws}, win_rate={self.win_rate:.1f}%)"
        )

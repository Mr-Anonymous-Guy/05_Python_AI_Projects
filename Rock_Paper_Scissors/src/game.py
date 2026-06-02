"""
game.py — Core game logic for Rock Paper Scissors.

Contains the round-result calculator and the GameSession class that
drives a single game (single-round, best-of-3, best-of-5, or unlimited).
"""

from typing import Literal, Optional

from src.player import ComputerPlayer, HumanPlayer, Player
from src.stats import Result, Stats
from src.utils import (
    CHOICE_EMOJI,
    SEPARATOR,
    get_input,
    get_menu_choice,
    print_separator,
)

# ──────────────────────────────────────────────────────────────
# Win / Loss / Draw logic
# ──────────────────────────────────────────────────────────────

# Maps each choice to the choice it defeats.
BEATS: dict[str, str] = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock",
}


def determine_winner(
    player_choice: str, computer_choice: str
) -> Result:
    """
    Determine the outcome of a single round.

    Args:
        player_choice:   The human player's move.
        computer_choice: The computer's move.

    Returns:
        "win"  – the human player wins.
        "loss" – the computer wins.
        "draw" – both players chose the same move.

    Raises:
        ValueError: If either choice is not a recognised move.
    """
    for choice in (player_choice, computer_choice):
        if choice not in BEATS:
            raise ValueError(f"Invalid choice: {choice!r}")

    if player_choice == computer_choice:
        return "draw"
    if BEATS[player_choice] == computer_choice:
        return "win"
    return "loss"


# ──────────────────────────────────────────────────────────────
# Game-mode definitions
# ──────────────────────────────────────────────────────────────

GameMode = Literal["single", "best_of_3", "best_of_5", "unlimited"]

MODE_LABELS: dict[str, str] = {
    "1": "Single Round",
    "2": "Best of 3",
    "3": "Best of 5",
    "4": "Unlimited",
}

MODE_KEYS: dict[str, GameMode] = {
    "1": "single",
    "2": "best_of_3",
    "3": "best_of_5",
    "4": "unlimited",
}

# Win target per mode (None = unlimited).
WIN_TARGET: dict[GameMode, Optional[int]] = {
    "single": 1,
    "best_of_3": 2,
    "best_of_5": 3,
    "unlimited": None,
}

# Maximum rounds per mode (None = unlimited).
MAX_ROUNDS: dict[GameMode, Optional[int]] = {
    "single": 1,
    "best_of_3": 3,
    "best_of_5": 5,
    "unlimited": None,
}


# ──────────────────────────────────────────────────────────────
# GameSession
# ──────────────────────────────────────────────────────────────


class GameSession:
    """
    Manages a single game session between a human and the computer.

    Attributes:
        mode:     The selected game mode.
        human:    The human player instance.
        computer: The computer player instance.
        session_stats: Stats accumulated during this session.
    """

    def __init__(self, mode: GameMode, human_name: str = "You") -> None:
        """
        Initialise the session.

        Args:
            mode:       Game mode to play.
            human_name: Display name for the human player.
        """
        self.mode: GameMode = mode
        self.human: Player = HumanPlayer(human_name)
        self.computer: Player = ComputerPlayer()
        self.session_stats: Stats = Stats()

    # ── public interface ────────────────────────────────────

    def play(self) -> Stats:
        """
        Run the full game session.

        Returns:
            The Stats object populated after the session ends.
        """
        self._print_mode_header()

        win_target = WIN_TARGET[self.mode]
        max_rounds = MAX_ROUNDS[self.mode]
        round_num = 0

        while True:
            round_num += 1
            self._play_round(round_num)

            # ── check termination conditions ────────────────
            if win_target and (
                self.session_stats.wins >= win_target
                or self.session_stats.losses >= win_target
            ):
                break

            if max_rounds and round_num >= max_rounds:
                break

            # ── unlimited mode: ask to continue ─────────────
            if self.mode == "unlimited":
                again = get_menu_choice(
                    "\n  Continue? [y] Yes  [n] No : ", {"y", "n"}
                )
                if again == "n":
                    break

        self._print_session_result()
        return self.session_stats

    # ── private helpers ─────────────────────────────────────

    def _play_round(self, round_num: int) -> None:
        """Execute one round and update session stats."""
        print(f"\n  {'─' * 36}")
        print(f"  Round {round_num}")
        print(f"  {'─' * 36}")

        human_choice = self.human.get_choice()
        computer_choice = self.computer.get_choice()

        result = determine_winner(human_choice, computer_choice)
        self.session_stats.record(result)

        self._display_round_result(human_choice, computer_choice, result)

    def _display_round_result(
        self, human_choice: str, computer_choice: str, result: Result
    ) -> None:
        """Print the moves and outcome for a single round."""
        h_emoji = CHOICE_EMOJI[human_choice]
        c_emoji = CHOICE_EMOJI[computer_choice]

        print(f"\n  {self.human.name:<14} {h_emoji}  {human_choice}")
        print(f"  {self.computer.name:<14} {c_emoji}  {computer_choice}")
        print()

        if result == "win":
            print("  🏆  You win this round!")
        elif result == "loss":
            print("  💻  Computer wins this round!")
        else:
            print("  🤝  It's a draw!")

        # Running score (shown for multi-round modes)
        if self.mode != "single":
            print(
                f"\n  Score →  You {self.session_stats.wins}"
                f"  :  {self.session_stats.losses}  Computer"
                f"  (Draws: {self.session_stats.draws})"
            )

    def _print_mode_header(self) -> None:
        """Print the game-mode header before the first round."""
        print_separator()
        print(f"  🎮  Mode: {MODE_LABELS[MODE_KEYS_REVERSED[self.mode]]}")
        print_separator()

    def _print_session_result(self) -> None:
        """Print the final session outcome banner."""
        print_separator()
        s = self.session_stats
        win_target = WIN_TARGET[self.mode]

        if self.mode == "single":
            if s.wins == 1:
                print("  🏆  RESULT: YOU WIN!")
            elif s.losses == 1:
                print("  💻  RESULT: COMPUTER WINS!")
            else:
                print("  🤝  RESULT: DRAW!")
        else:
            if win_target and s.wins >= win_target:
                print("  🏆  RESULT: YOU WIN THE MATCH!")
            elif win_target and s.losses >= win_target:
                print("  💻  RESULT: COMPUTER WINS THE MATCH!")
            else:
                if s.wins > s.losses:
                    print("  🏆  RESULT: YOU WIN THE MATCH!")
                elif s.losses > s.wins:
                    print("  💻  RESULT: COMPUTER WINS THE MATCH!")
                else:
                    print("  🤝  RESULT: MATCH IS A DRAW!")

        print(s.summary("Session Stats"))


# ──────────────────────────────────────────────────────────────
# Reverse lookup helper (mode → menu key)
# ──────────────────────────────────────────────────────────────

MODE_KEYS_REVERSED: dict[GameMode, str] = {v: k for k, v in MODE_KEYS.items()}

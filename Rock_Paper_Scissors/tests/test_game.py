"""
test_game.py — Unit tests for Rock Paper Scissors.

Covers:
  - determine_winner()  (winner calculation)
  - validate_choice()   (input validation)
  - Stats               (score tracking)
  - GameSession         (integration smoke-test)
"""

import sys
import os
import unittest
from unittest.mock import patch

# ── path setup ──────────────────────────────────────────────────────────────
# Allow running tests from the project root or the tests/ directory.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.game import GameSession, determine_winner
from src.stats import Stats
from src.utils import validate_choice


# ═══════════════════════════════════════════════════════════════════════════
# 1. Winner calculation
# ═══════════════════════════════════════════════════════════════════════════


class TestDetermineWinner(unittest.TestCase):
    """Tests for the determine_winner() pure function."""

    # ── wins ────────────────────────────────────────────────
    def test_rock_beats_scissors(self) -> None:
        self.assertEqual(determine_winner("Rock", "Scissors"), "win")

    def test_scissors_beats_paper(self) -> None:
        self.assertEqual(determine_winner("Scissors", "Paper"), "win")

    def test_paper_beats_rock(self) -> None:
        self.assertEqual(determine_winner("Paper", "Rock"), "win")

    # ── losses ──────────────────────────────────────────────
    def test_scissors_loses_to_rock(self) -> None:
        self.assertEqual(determine_winner("Scissors", "Rock"), "loss")

    def test_paper_loses_to_scissors(self) -> None:
        self.assertEqual(determine_winner("Paper", "Scissors"), "loss")

    def test_rock_loses_to_paper(self) -> None:
        self.assertEqual(determine_winner("Rock", "Paper"), "loss")

    # ── draws ───────────────────────────────────────────────
    def test_rock_draw(self) -> None:
        self.assertEqual(determine_winner("Rock", "Rock"), "draw")

    def test_paper_draw(self) -> None:
        self.assertEqual(determine_winner("Paper", "Paper"), "draw")

    def test_scissors_draw(self) -> None:
        self.assertEqual(determine_winner("Scissors", "Scissors"), "draw")

    # ── invalid input ────────────────────────────────────────
    def test_invalid_player_choice_raises(self) -> None:
        with self.assertRaises(ValueError):
            determine_winner("Fire", "Rock")

    def test_invalid_computer_choice_raises(self) -> None:
        with self.assertRaises(ValueError):
            determine_winner("Rock", "Water")

    def test_both_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            determine_winner("Lizard", "Spock")


# ═══════════════════════════════════════════════════════════════════════════
# 2. Input validation
# ═══════════════════════════════════════════════════════════════════════════


class TestValidateChoice(unittest.TestCase):
    """Tests for the validate_choice() utility function."""

    # ── numeric shortcuts ────────────────────────────────────
    def test_numeric_1_maps_to_rock(self) -> None:
        self.assertEqual(validate_choice("1"), "Rock")

    def test_numeric_2_maps_to_paper(self) -> None:
        self.assertEqual(validate_choice("2"), "Paper")

    def test_numeric_3_maps_to_scissors(self) -> None:
        self.assertEqual(validate_choice("3"), "Scissors")

    # ── letter shortcuts ─────────────────────────────────────
    def test_r_maps_to_rock(self) -> None:
        self.assertEqual(validate_choice("r"), "Rock")

    def test_p_maps_to_paper(self) -> None:
        self.assertEqual(validate_choice("p"), "Paper")

    def test_s_maps_to_scissors(self) -> None:
        self.assertEqual(validate_choice("s"), "Scissors")

    # ── full words ───────────────────────────────────────────
    def test_full_word_rock(self) -> None:
        self.assertEqual(validate_choice("rock"), "Rock")

    def test_full_word_paper(self) -> None:
        self.assertEqual(validate_choice("paper"), "Paper")

    def test_full_word_scissors(self) -> None:
        self.assertEqual(validate_choice("scissors"), "Scissors")

    # ── case-insensitivity ───────────────────────────────────
    def test_uppercase_rock(self) -> None:
        self.assertEqual(validate_choice("ROCK"), "Rock")

    def test_mixed_case_paper(self) -> None:
        self.assertEqual(validate_choice("PaPeR"), "Paper")

    # ── invalid inputs ───────────────────────────────────────
    def test_empty_string_returns_none(self) -> None:
        self.assertIsNone(validate_choice(""))

    def test_random_text_returns_none(self) -> None:
        self.assertIsNone(validate_choice("banana"))

    def test_number_4_returns_none(self) -> None:
        self.assertIsNone(validate_choice("4"))

    def test_whitespace_returns_none(self) -> None:
        self.assertIsNone(validate_choice("   "))


# ═══════════════════════════════════════════════════════════════════════════
# 3. Score / Stats updates
# ═══════════════════════════════════════════════════════════════════════════


class TestStats(unittest.TestCase):
    """Tests for the Stats dataclass."""

    def setUp(self) -> None:
        self.stats = Stats()

    # ── record ───────────────────────────────────────────────
    def test_record_win(self) -> None:
        self.stats.record("win")
        self.assertEqual(self.stats.wins, 1)

    def test_record_loss(self) -> None:
        self.stats.record("loss")
        self.assertEqual(self.stats.losses, 1)

    def test_record_draw(self) -> None:
        self.stats.record("draw")
        self.assertEqual(self.stats.draws, 1)

    def test_record_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.stats.record("tie")  # type: ignore[arg-type]

    # ── total ────────────────────────────────────────────────
    def test_total_accumulates(self) -> None:
        self.stats.record("win")
        self.stats.record("loss")
        self.stats.record("draw")
        self.assertEqual(self.stats.total, 3)

    # ── win_rate ─────────────────────────────────────────────
    def test_win_rate_zero_when_no_games(self) -> None:
        self.assertAlmostEqual(self.stats.win_rate, 0.0)

    def test_win_rate_100_all_wins(self) -> None:
        for _ in range(5):
            self.stats.record("win")
        self.assertAlmostEqual(self.stats.win_rate, 100.0)

    def test_win_rate_50_percent(self) -> None:
        self.stats.record("win")
        self.stats.record("loss")
        self.assertAlmostEqual(self.stats.win_rate, 50.0)

    def test_win_rate_rounds_correctly(self) -> None:
        self.stats.record("win")
        self.stats.record("loss")
        self.stats.record("loss")
        # 1/3 ≈ 33.33 %
        self.assertAlmostEqual(self.stats.win_rate, 33.333, places=1)

    # ── reset ────────────────────────────────────────────────
    def test_reset_clears_all(self) -> None:
        self.stats.record("win")
        self.stats.record("loss")
        self.stats.reset()
        self.assertEqual(self.stats.wins, 0)
        self.assertEqual(self.stats.losses, 0)
        self.assertEqual(self.stats.draws, 0)

    # ── merge ────────────────────────────────────────────────
    def test_merge_combines_stats(self) -> None:
        other = Stats(wins=3, losses=1, draws=2)
        self.stats.record("win")
        self.stats.merge(other)
        self.assertEqual(self.stats.wins, 4)
        self.assertEqual(self.stats.losses, 1)
        self.assertEqual(self.stats.draws, 2)

    # ── summary ──────────────────────────────────────────────
    def test_summary_contains_key_fields(self) -> None:
        self.stats.record("win")
        summary = self.stats.summary()
        self.assertIn("Wins", summary)
        self.assertIn("Losses", summary)
        self.assertIn("Win Rate", summary)


# ═══════════════════════════════════════════════════════════════════════════
# 4. GameSession integration smoke-tests
# ═══════════════════════════════════════════════════════════════════════════


class TestGameSession(unittest.TestCase):
    """Integration-level smoke-tests for GameSession."""

    def _run_session(self, mode: str, human_moves: list[str], computer_moves: list[str]) -> Stats:
        """Helper: run a session with predetermined moves."""
        session = GameSession(mode)  # type: ignore[arg-type]
        with (
            patch("src.utils.get_valid_choice", side_effect=human_moves),
            patch("src.player.random.choice", side_effect=computer_moves),
        ):
            return session.play()

    def test_single_round_win(self) -> None:
        stats = self._run_session("single", ["Rock"], ["Scissors"])
        self.assertEqual(stats.wins, 1)
        self.assertEqual(stats.total, 1)

    def test_single_round_loss(self) -> None:
        stats = self._run_session("single", ["Scissors"], ["Rock"])
        self.assertEqual(stats.losses, 1)

    def test_single_round_draw(self) -> None:
        stats = self._run_session("single", ["Paper"], ["Paper"])
        self.assertEqual(stats.draws, 1)

    def test_best_of_3_player_wins(self) -> None:
        # Human wins rounds 1 and 2 → session ends early
        stats = self._run_session(
            "best_of_3",
            ["Rock", "Rock"],
            ["Scissors", "Scissors"],
        )
        self.assertEqual(stats.wins, 2)

    def test_best_of_5_computer_wins(self) -> None:
        # Computer wins 3 rounds
        stats = self._run_session(
            "best_of_5",
            ["Scissors", "Scissors", "Scissors"],
            ["Rock", "Rock", "Rock"],
        )
        self.assertEqual(stats.losses, 3)

    def test_stats_total_matches_rounds_played(self) -> None:
        stats = self._run_session(
            "best_of_3",
            ["Rock", "Scissors", "Paper"],
            ["Scissors", "Rock", "Paper"],
        )
        # Wins: 1 (Rd1), Losses: 1 (Rd2), Draw: 1 (Rd3) — neither wins 2 → 3 rounds
        self.assertEqual(stats.total, 3)


# ──────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)

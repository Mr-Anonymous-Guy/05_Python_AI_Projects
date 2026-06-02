"""
test_strength.py — Unit tests for strength.py

Covers:
  - Individual scoring helpers
  - Rating thresholds
  - analyse() on known passwords
  - StrengthReport properties and display
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.strength import (
    StrengthReport,
    _char_score,
    _length_score,
    _rating_from_score,
    _variety_score,
    analyse,
)


class TestLengthScore(unittest.TestCase):
    """Tests for _length_score()."""

    def test_zero_length(self) -> None:
        self.assertEqual(_length_score(0), 0)

    def test_short_password(self) -> None:
        score = _length_score(4)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 40)

    def test_long_password_caps_at_40(self) -> None:
        self.assertLessEqual(_length_score(512), 40)

    def test_longer_scores_higher(self) -> None:
        self.assertGreater(_length_score(16), _length_score(8))

    def test_max_score_at_32_or_above(self) -> None:
        self.assertEqual(_length_score(32), 40)


class TestCharScore(unittest.TestCase):
    """Tests for _char_score()."""

    def test_zero_count_gives_zero(self) -> None:
        self.assertEqual(_char_score(0, 10), 0)

    def test_one_count_gives_half(self) -> None:
        self.assertEqual(_char_score(1, 10), 5)

    def test_two_or_more_gives_max(self) -> None:
        self.assertEqual(_char_score(2, 10), 10)
        self.assertEqual(_char_score(100, 10), 10)

    def test_different_max_values(self) -> None:
        self.assertEqual(_char_score(0, 15), 0)
        self.assertEqual(_char_score(1, 15), 7)
        self.assertEqual(_char_score(3, 15), 15)


class TestVarietyScore(unittest.TestCase):
    """Tests for _variety_score()."""

    def test_zero_total_returns_zero(self) -> None:
        self.assertEqual(_variety_score(0, 0), 0)

    def test_all_unique_returns_max(self) -> None:
        self.assertEqual(_variety_score(15, 15), 15)

    def test_partial_variety(self) -> None:
        score = _variety_score(5, 10)  # 50 % unique → 7
        self.assertEqual(score, 7)

    def test_no_variety_returns_zero(self) -> None:
        self.assertEqual(_variety_score(1, 10), 1)

    def test_caps_at_15(self) -> None:
        self.assertLessEqual(_variety_score(100, 100), 15)


class TestRatingFromScore(unittest.TestCase):
    """Tests for _rating_from_score()."""

    def test_very_weak_boundary(self) -> None:
        self.assertEqual(_rating_from_score(0),  "Very Weak")
        self.assertEqual(_rating_from_score(19), "Very Weak")

    def test_weak_boundary(self) -> None:
        self.assertEqual(_rating_from_score(20), "Weak")
        self.assertEqual(_rating_from_score(39), "Weak")

    def test_fair_boundary(self) -> None:
        self.assertEqual(_rating_from_score(40), "Fair")
        self.assertEqual(_rating_from_score(59), "Fair")

    def test_strong_boundary(self) -> None:
        self.assertEqual(_rating_from_score(60), "Strong")
        self.assertEqual(_rating_from_score(79), "Strong")

    def test_very_strong_boundary(self) -> None:
        self.assertEqual(_rating_from_score(80),  "Very Strong")
        self.assertEqual(_rating_from_score(100), "Very Strong")


class TestAnalyse(unittest.TestCase):
    """Tests for the public analyse() function."""

    # ── basic field correctness ────────────────────────────────

    def test_empty_password(self) -> None:
        report = analyse("")
        self.assertEqual(report.length, 0)
        self.assertEqual(report.score,  0)
        self.assertEqual(report.rating, "Very Weak")

    def test_all_lowercase(self) -> None:
        report = analyse("abcdefghij")
        self.assertEqual(report.upper_count,  0)
        self.assertGreater(report.lower_count, 0)
        self.assertEqual(report.digit_count,  0)
        self.assertEqual(report.symbol_count, 0)

    def test_all_uppercase(self) -> None:
        report = analyse("ABCDEFGHIJ")
        self.assertGreater(report.upper_count, 0)
        self.assertEqual(report.lower_count,  0)

    def test_all_digits(self) -> None:
        report = analyse("1234567890")
        self.assertGreater(report.digit_count, 0)
        self.assertEqual(report.symbol_count, 0)

    def test_all_symbols(self) -> None:
        report = analyse("!@#$%^&*()")
        self.assertGreater(report.symbol_count, 0)

    # ── score ordering ─────────────────────────────────────────

    def test_longer_password_scores_higher(self) -> None:
        short = analyse("Ab1!")
        long  = analyse("Ab1!Ab1!Ab1!Ab1!")
        self.assertGreater(long.score, short.score)

    def test_complex_password_stronger_than_simple(self) -> None:
        simple  = analyse("aaaaaaaa")
        complex_ = analyse("Aa1!Bb2@")
        self.assertGreater(complex_.score, simple.score)

    # ── unique count ───────────────────────────────────────────

    def test_unique_count_correct(self) -> None:
        report = analyse("aabbcc")
        self.assertEqual(report.unique_count, 3)

    def test_unique_count_all_same(self) -> None:
        report = analyse("aaaa")
        self.assertEqual(report.unique_count, 1)

    # ── variety_count property ────────────────────────────────

    def test_variety_count_four(self) -> None:
        report = analyse("Aa1!")
        self.assertEqual(report.variety_count, 4)

    def test_variety_count_one(self) -> None:
        report = analyse("aaaa")
        self.assertEqual(report.variety_count, 1)

    # ── suggestions ────────────────────────────────────────────

    def test_suggestions_present_for_weak_password(self) -> None:
        report = analyse("aaaa")
        self.assertGreater(len(report.suggestions), 0)

    def test_no_suggestions_for_strong_password(self) -> None:
        # Long password with all categories
        report = analyse("Aa1!Bb2@Cc3#Dd4$Ee5%Ff6^")
        self.assertEqual(report.suggestions, [])

    def test_suggestion_mentions_uppercase_when_missing(self) -> None:
        report = analyse("abcdefgh12!")
        tips = " ".join(report.suggestions).lower()
        self.assertIn("uppercase", tips)

    # ── display ────────────────────────────────────────────────

    def test_display_contains_score(self) -> None:
        report = analyse("TestPassword1!")
        display = report.display()
        self.assertIn(str(report.score), display)

    def test_display_contains_rating(self) -> None:
        report = analyse("TestPassword1!")
        display = report.display()
        self.assertIn(report.rating, display)

    def test_display_contains_password(self) -> None:
        pw = "TestPassword1!"
        report = analyse(pw)
        self.assertIn(pw, report.display())

    # ── rating emoji ───────────────────────────────────────────

    def test_rating_emoji_not_empty(self) -> None:
        for pw in ("a", "aaaa", "Aa1!Bb2@Cc3#"):
            with self.subTest(pw=pw):
                self.assertNotEqual(analyse(pw).rating_emoji, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

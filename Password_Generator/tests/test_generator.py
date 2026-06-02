"""
test_generator.py — Unit tests for generator.py

Covers:
  - Password length enforcement
  - Character-category guarantee (at least one of each enabled type)
  - Charset construction
  - Bulk generation
  - Error handling on invalid config
"""

import string
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.generator import (
    POOL_DIGITS,
    POOL_LOWER,
    POOL_SYMBOLS,
    POOL_UPPER,
    PasswordConfig,
    generate_bulk,
    generate_password,
)


class TestPasswordConfig(unittest.TestCase):
    """Tests for PasswordConfig.charset()."""

    def test_all_categories_enabled(self) -> None:
        cfg = PasswordConfig(use_upper=True, use_lower=True, use_digits=True, use_symbols=True)
        cs = cfg.charset()
        self.assertTrue(any(c in POOL_UPPER   for c in cs))
        self.assertTrue(any(c in POOL_LOWER   for c in cs))
        self.assertTrue(any(c in POOL_DIGITS  for c in cs))
        self.assertTrue(any(c in POOL_SYMBOLS for c in cs))

    def test_only_upper(self) -> None:
        cfg = PasswordConfig(use_upper=True, use_lower=False, use_digits=False, use_symbols=False)
        cs = cfg.charset()
        self.assertTrue(all(c in POOL_UPPER for c in cs))

    def test_only_digits(self) -> None:
        cfg = PasswordConfig(use_upper=False, use_lower=False, use_digits=True, use_symbols=False)
        cs = cfg.charset()
        self.assertTrue(all(c in POOL_DIGITS for c in cs))

    def test_empty_charset_raises(self) -> None:
        cfg = PasswordConfig(use_upper=False, use_lower=False, use_digits=False, use_symbols=False)
        with self.assertRaises(ValueError):
            cfg.charset()


class TestGeneratePassword(unittest.TestCase):
    """Tests for generate_password()."""

    # ── length ─────────────────────────────────────────────────

    def test_correct_length_default(self) -> None:
        cfg = PasswordConfig()
        self.assertEqual(len(generate_password(cfg)), 16)

    def test_correct_length_custom(self) -> None:
        for length in (4, 8, 20, 64, 128):
            with self.subTest(length=length):
                cfg = PasswordConfig(length=length)
                self.assertEqual(len(generate_password(cfg)), length)

    # ── category guarantees ────────────────────────────────────

    def test_contains_uppercase_when_enabled(self) -> None:
        cfg = PasswordConfig(length=20, use_upper=True)
        pw = generate_password(cfg)
        self.assertTrue(any(c in POOL_UPPER for c in pw))

    def test_contains_lowercase_when_enabled(self) -> None:
        cfg = PasswordConfig(length=20, use_lower=True, use_upper=False, use_digits=False, use_symbols=False)
        pw = generate_password(cfg)
        self.assertTrue(any(c in POOL_LOWER for c in pw))

    def test_contains_digit_when_enabled(self) -> None:
        cfg = PasswordConfig(length=20, use_digits=True, use_upper=False, use_lower=False, use_symbols=False)
        pw = generate_password(cfg)
        self.assertTrue(any(c in POOL_DIGITS for c in pw))

    def test_contains_symbol_when_enabled(self) -> None:
        cfg = PasswordConfig(length=20, use_symbols=True, use_upper=False, use_lower=False, use_digits=False)
        pw = generate_password(cfg)
        self.assertTrue(any(c in POOL_SYMBOLS for c in pw))

    def test_no_uppercase_when_disabled(self) -> None:
        cfg = PasswordConfig(length=50, use_upper=False, use_lower=True, use_digits=True, use_symbols=False)
        for _ in range(10):
            pw = generate_password(cfg)
            self.assertFalse(any(c in POOL_UPPER for c in pw))

    def test_no_symbols_when_disabled(self) -> None:
        cfg = PasswordConfig(length=50, use_upper=True, use_lower=True, use_digits=True, use_symbols=False)
        for _ in range(10):
            pw = generate_password(cfg)
            self.assertFalse(any(c in POOL_SYMBOLS for c in pw))

    # ── uniqueness / randomness ────────────────────────────────

    def test_two_passwords_are_different(self) -> None:
        cfg = PasswordConfig(length=20)
        pw1 = generate_password(cfg)
        pw2 = generate_password(cfg)
        # Extremely unlikely to collide for length 20
        self.assertNotEqual(pw1, pw2)

    # ── error handling ─────────────────────────────────────────

    def test_invalid_length_raises(self) -> None:
        cfg = PasswordConfig(length=2)  # below MIN_LENGTH
        with self.assertRaises(ValueError):
            generate_password(cfg)

    def test_empty_charset_raises(self) -> None:
        cfg = PasswordConfig(use_upper=False, use_lower=False, use_digits=False, use_symbols=False)
        with self.assertRaises(ValueError):
            generate_password(cfg)

    # ── charset integrity ──────────────────────────────────────

    def test_all_chars_in_charset(self) -> None:
        cfg = PasswordConfig(length=100, use_upper=True, use_lower=True, use_digits=True, use_symbols=False)
        allowed = set(cfg.charset())
        pw = generate_password(cfg)
        self.assertTrue(all(c in allowed for c in pw))


class TestGenerateBulk(unittest.TestCase):
    """Tests for generate_bulk()."""

    def test_returns_correct_count(self) -> None:
        cfg = PasswordConfig()
        passwords = generate_bulk(cfg, 10)
        self.assertEqual(len(passwords), 10)

    def test_all_correct_length(self) -> None:
        cfg = PasswordConfig(length=12)
        for pw in generate_bulk(cfg, 5):
            self.assertEqual(len(pw), 12)

    def test_count_zero_raises(self) -> None:
        cfg = PasswordConfig()
        with self.assertRaises(ValueError):
            generate_bulk(cfg, 0)

    def test_count_one(self) -> None:
        cfg = PasswordConfig()
        result = generate_bulk(cfg, 1)
        self.assertEqual(len(result), 1)

    def test_large_bulk(self) -> None:
        cfg = PasswordConfig(length=8)
        passwords = generate_bulk(cfg, 100)
        self.assertEqual(len(passwords), 100)
        # All should be strings of correct length
        self.assertTrue(all(isinstance(p, str) and len(p) == 8 for p in passwords))


if __name__ == "__main__":
    unittest.main(verbosity=2)

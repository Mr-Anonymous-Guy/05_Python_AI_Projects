"""
test_validator.py — Unit tests for validator.py

Covers:
  - validate_length()
  - validate_charset()
  - validate_bulk_count()
  - validate_generation_request()
  - ValidationResult behaviour
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.validator import (
    MAX_BULK,
    MAX_LENGTH,
    MIN_LENGTH,
    ValidationResult,
    validate_bulk_count,
    validate_charset,
    validate_generation_request,
    validate_length,
)


class TestValidationResult(unittest.TestCase):
    """Tests for the ValidationResult helper dataclass."""

    def test_default_is_ok(self) -> None:
        vr = ValidationResult()
        self.assertTrue(vr.ok)
        self.assertEqual(vr.errors, [])

    def test_add_error_sets_ok_false(self) -> None:
        vr = ValidationResult()
        vr.add_error("Something went wrong.")
        self.assertFalse(vr.ok)

    def test_multiple_errors_accumulate(self) -> None:
        vr = ValidationResult()
        vr.add_error("Error 1")
        vr.add_error("Error 2")
        self.assertEqual(len(vr.errors), 2)

    def test_first_error_property(self) -> None:
        vr = ValidationResult()
        vr.add_error("First")
        vr.add_error("Second")
        self.assertEqual(vr.first_error, "First")

    def test_first_error_none_when_empty(self) -> None:
        vr = ValidationResult()
        self.assertIsNone(vr.first_error)

    def test_bool_true_when_ok(self) -> None:
        self.assertTrue(bool(ValidationResult()))

    def test_bool_false_after_error(self) -> None:
        vr = ValidationResult()
        vr.add_error("fail")
        self.assertFalse(bool(vr))


class TestValidateLength(unittest.TestCase):
    """Tests for validate_length()."""

    def test_min_length_is_valid(self) -> None:
        self.assertTrue(validate_length(MIN_LENGTH))

    def test_max_length_is_valid(self) -> None:
        self.assertTrue(validate_length(MAX_LENGTH))

    def test_typical_length_valid(self) -> None:
        for n in (8, 12, 16, 32, 64):
            with self.subTest(n=n):
                self.assertTrue(validate_length(n))

    def test_below_minimum_invalid(self) -> None:
        self.assertFalse(validate_length(MIN_LENGTH - 1))

    def test_zero_invalid(self) -> None:
        self.assertFalse(validate_length(0))

    def test_negative_invalid(self) -> None:
        self.assertFalse(validate_length(-5))

    def test_above_maximum_invalid(self) -> None:
        self.assertFalse(validate_length(MAX_LENGTH + 1))

    def test_error_message_mentions_minimum(self) -> None:
        vr = validate_length(1)
        self.assertTrue(any(str(MIN_LENGTH) in e for e in vr.errors))

    def test_error_message_mentions_maximum(self) -> None:
        vr = validate_length(MAX_LENGTH + 100)
        self.assertTrue(any(str(MAX_LENGTH) in e for e in vr.errors))


class TestValidateCharset(unittest.TestCase):
    """Tests for validate_charset()."""

    def test_all_true_valid(self) -> None:
        self.assertTrue(validate_charset(True, True, True, True))

    def test_single_true_valid(self) -> None:
        self.assertTrue(validate_charset(True, False, False, False))
        self.assertTrue(validate_charset(False, True, False, False))
        self.assertTrue(validate_charset(False, False, True, False))
        self.assertTrue(validate_charset(False, False, False, True))

    def test_all_false_invalid(self) -> None:
        self.assertFalse(validate_charset(False, False, False, False))

    def test_error_message_on_empty_charset(self) -> None:
        vr = validate_charset(False, False, False, False)
        self.assertTrue(len(vr.errors) > 0)


class TestValidateBulkCount(unittest.TestCase):
    """Tests for validate_bulk_count()."""

    def test_one_is_valid(self) -> None:
        self.assertTrue(validate_bulk_count(1))

    def test_max_bulk_is_valid(self) -> None:
        self.assertTrue(validate_bulk_count(MAX_BULK))

    def test_zero_invalid(self) -> None:
        self.assertFalse(validate_bulk_count(0))

    def test_negative_invalid(self) -> None:
        self.assertFalse(validate_bulk_count(-1))

    def test_above_max_invalid(self) -> None:
        self.assertFalse(validate_bulk_count(MAX_BULK + 1))

    def test_typical_count_valid(self) -> None:
        for n in (5, 10, 50, 100, 500):
            with self.subTest(n=n):
                self.assertTrue(validate_bulk_count(n))


class TestValidateGenerationRequest(unittest.TestCase):
    """Tests for the combined validate_generation_request()."""

    def test_valid_request_passes(self) -> None:
        vr = validate_generation_request(16, True, True, True, True)
        self.assertTrue(vr)

    def test_invalid_length_fails(self) -> None:
        vr = validate_generation_request(2, True, True, True, True)
        self.assertFalse(vr)

    def test_empty_charset_fails(self) -> None:
        vr = validate_generation_request(16, False, False, False, False)
        self.assertFalse(vr)

    def test_both_invalid_returns_two_errors(self) -> None:
        vr = validate_generation_request(1, False, False, False, False)
        self.assertFalse(vr)
        self.assertGreaterEqual(len(vr.errors), 2)

    def test_min_length_with_one_category(self) -> None:
        vr = validate_generation_request(MIN_LENGTH, True, False, False, False)
        self.assertTrue(vr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

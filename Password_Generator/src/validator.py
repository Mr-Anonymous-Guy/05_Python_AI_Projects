"""
validator.py — Input validation for password generation requests.

All validation is pure (no I/O) so it can be unit-tested easily
and reused across CLI and any future programmatic interface.
"""

from dataclasses import dataclass, field
from typing import Optional

# ──────────────────────────────────────────────────────────────
# Constraints
# ──────────────────────────────────────────────────────────────

MIN_LENGTH: int = 4       # Absolute minimum (security floor)
MAX_LENGTH: int = 512     # Practical maximum for bulk generation
MIN_BULK:   int = 1
MAX_BULK:   int = 1_000   # Cap on bulk generation requests


# ──────────────────────────────────────────────────────────────
# Validation result
# ──────────────────────────────────────────────────────────────


@dataclass
class ValidationResult:
    """
    Carries validation outcome and any error messages.

    Attributes:
        ok:     True when validation passed.
        errors: List of human-readable error strings (empty on success).
    """

    ok: bool = True
    errors: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """
        Record an error and mark the result as failed.

        Args:
            message: Human-readable description of the problem.
        """
        self.ok = False
        self.errors.append(message)

    @property
    def first_error(self) -> Optional[str]:
        """Return the first error message, or None if there are none."""
        return self.errors[0] if self.errors else None

    def __bool__(self) -> bool:
        return self.ok


# ──────────────────────────────────────────────────────────────
# Public validators
# ──────────────────────────────────────────────────────────────


def validate_length(length: int) -> ValidationResult:
    """
    Validate a requested password length.

    Rules:
    - Must be an integer (enforced by type hint).
    - Must be >= MIN_LENGTH.
    - Must be <= MAX_LENGTH.

    Args:
        length: Requested password length.

    Returns:
        ValidationResult with ok=True on success.
    """
    result = ValidationResult()

    if length < MIN_LENGTH:
        result.add_error(
            f"Password length must be at least {MIN_LENGTH} characters "
            f"(got {length})."
        )
    if length > MAX_LENGTH:
        result.add_error(
            f"Password length must not exceed {MAX_LENGTH} characters "
            f"(got {length})."
        )
    return result


def validate_charset(
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
) -> ValidationResult:
    """
    Validate that at least one character category is selected.

    Args:
        use_upper:   Include uppercase letters.
        use_lower:   Include lowercase letters.
        use_digits:  Include numeric digits.
        use_symbols: Include special symbols.

    Returns:
        ValidationResult with ok=True when at least one flag is True.
    """
    result = ValidationResult()
    if not any([use_upper, use_lower, use_digits, use_symbols]):
        result.add_error(
            "At least one character type must be selected "
            "(uppercase, lowercase, digits, or symbols)."
        )
    return result


def validate_bulk_count(count: int) -> ValidationResult:
    """
    Validate a bulk-generation count.

    Args:
        count: Number of passwords requested.

    Returns:
        ValidationResult with ok=True when count is in [MIN_BULK, MAX_BULK].
    """
    result = ValidationResult()
    if count < MIN_BULK:
        result.add_error(
            f"Count must be at least {MIN_BULK} (got {count})."
        )
    if count > MAX_BULK:
        result.add_error(
            f"Count must not exceed {MAX_BULK} (got {count})."
        )
    return result


def validate_generation_request(
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
) -> ValidationResult:
    """
    Combined validation for a single password generation request.

    Runs both length and charset checks and merges all errors.

    Args:
        length:      Requested password length.
        use_upper:   Include uppercase letters.
        use_lower:   Include lowercase letters.
        use_digits:  Include numeric digits.
        use_symbols: Include special symbols.

    Returns:
        ValidationResult — ok=True only when all sub-checks pass.
    """
    combined = ValidationResult()

    for result in (
        validate_length(length),
        validate_charset(use_upper, use_lower, use_digits, use_symbols),
    ):
        for error in result.errors:
            combined.add_error(error)

    return combined

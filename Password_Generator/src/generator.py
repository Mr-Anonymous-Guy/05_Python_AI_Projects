"""
generator.py — Cryptographically secure password generation engine.

Uses ``secrets`` (Python 3.6+) instead of ``random`` to ensure that
generated passwords are suitable for security-sensitive contexts.

Teaching note
─────────────
``secrets.choice()`` reads from the OS CSPRNG (e.g., /dev/urandom on
Linux, CryptGenRandom on Windows) and is therefore unpredictable by
an attacker — unlike ``random.choice()`` which is a pseudo-RNG seeded
from system time.
"""

import secrets
import string
from dataclasses import dataclass

from src.validator import validate_generation_request

# ──────────────────────────────────────────────────────────────
# Character pool constants
# ──────────────────────────────────────────────────────────────

POOL_UPPER:   str = string.ascii_uppercase          # A–Z
POOL_LOWER:   str = string.ascii_lowercase          # a–z
POOL_DIGITS:  str = string.digits                   # 0–9
POOL_SYMBOLS: str = string.punctuation              # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~


# ──────────────────────────────────────────────────────────────
# Configuration dataclass
# ──────────────────────────────────────────────────────────────


@dataclass
class PasswordConfig:
    """
    Immutable configuration for a password generation request.

    Attributes:
        length:      Number of characters in each password.
        use_upper:   Include uppercase letters.
        use_lower:   Include lowercase letters.
        use_digits:  Include numeric digits.
        use_symbols: Include punctuation / special characters.
    """

    length: int      = 16
    use_upper: bool  = True
    use_lower: bool  = True
    use_digits: bool = True
    use_symbols: bool = True

    def charset(self) -> str:
        """
        Build and return the full character pool for this config.

        Returns:
            Concatenated string of all enabled character categories.

        Raises:
            ValueError: If no category is enabled (empty charset).
        """
        pool = ""
        if self.use_upper:
            pool += POOL_UPPER
        if self.use_lower:
            pool += POOL_LOWER
        if self.use_digits:
            pool += POOL_DIGITS
        if self.use_symbols:
            pool += POOL_SYMBOLS

        if not pool:
            raise ValueError(
                "At least one character category must be enabled."
            )
        return pool


# ──────────────────────────────────────────────────────────────
# Core generation functions
# ──────────────────────────────────────────────────────────────


def generate_password(config: PasswordConfig) -> str:
    """
    Generate a single cryptographically secure password.

    The algorithm guarantees that at least one character from each
    enabled category is included, preventing the (unlikely but
    possible) case where ``secrets.choice`` never picks a required
    category in a short password.

    Args:
        config: A PasswordConfig instance describing the requirements.

    Returns:
        A password string of exactly ``config.length`` characters.

    Raises:
        ValueError: If the config fails validation (see validator.py).
    """
    result = validate_generation_request(
        config.length,
        config.use_upper,
        config.use_lower,
        config.use_digits,
        config.use_symbols,
    )
    if not result:
        raise ValueError(result.first_error)

    charset = config.charset()

    # ── guarantee representation ─────────────────────────────
    mandatory: list[str] = []
    if config.use_upper:
        mandatory.append(secrets.choice(POOL_UPPER))
    if config.use_lower:
        mandatory.append(secrets.choice(POOL_LOWER))
    if config.use_digits:
        mandatory.append(secrets.choice(POOL_DIGITS))
    if config.use_symbols:
        mandatory.append(secrets.choice(POOL_SYMBOLS))

    # ── fill remaining length from full charset ───────────────
    remaining = config.length - len(mandatory)
    filler = [secrets.choice(charset) for _ in range(remaining)]

    # ── shuffle to avoid predictable positions ────────────────
    password_chars = mandatory + filler
    # secrets.SystemRandom is CSPRNG-backed
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


def generate_bulk(config: PasswordConfig, count: int) -> list[str]:
    """
    Generate multiple passwords with the same configuration.

    Args:
        config: Password configuration shared by all generated passwords.
        count:  Number of passwords to generate.

    Returns:
        A list of unique password strings.

    Raises:
        ValueError: On invalid config or count < 1.
    """
    if count < 1:
        raise ValueError(f"Count must be at least 1 (got {count}).")

    return [generate_password(config) for _ in range(count)]

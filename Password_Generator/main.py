"""
main.py — CLI entry point for the Password Generator.

Run with:
    python main.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generator import PasswordConfig, generate_bulk, generate_password
from src.strength import analyse
from src.utils import (
    clear_screen,
    confirm,
    get_input,
    get_int_input,
    get_menu_choice,
    print_banner,
    print_error,
    print_info,
    print_separator,
    print_success,
)
from src.validator import (
    MAX_BULK,
    MAX_LENGTH,
    MIN_LENGTH,
    validate_bulk_count,
    validate_generation_request,
)

# ──────────────────────────────────────────────────────────────
# Clipboard support (optional — pyperclip)
# ──────────────────────────────────────────────────────────────

try:
    import pyperclip  # type: ignore[import]
    _CLIPBOARD_AVAILABLE = True
except ImportError:
    _CLIPBOARD_AVAILABLE = False


def _copy_to_clipboard(text: str) -> bool:
    """
    Copy text to the system clipboard if pyperclip is installed.

    Args:
        text: The string to copy.

    Returns:
        True on success, False when pyperclip is not available.
    """
    if not _CLIPBOARD_AVAILABLE:
        return False
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False


# ──────────────────────────────────────────────────────────────
# Configuration builder
# ──────────────────────────────────────────────────────────────


def _collect_config() -> Optional[PasswordConfig]:
    """
    Interactively collect password generation options from the user.

    Returns:
        A validated PasswordConfig, or None if the user cancels.
    """
    print()
    print_separator()
    print("  ⚙️   Password Configuration")
    print_separator()

    # ── length ────────────────────────────────────────────────
    while True:
        length = get_int_input(
            f"  Length ({MIN_LENGTH}–{MAX_LENGTH}) [default 16]: ",
            min_val=MIN_LENGTH,
            max_val=MAX_LENGTH,
        )
        if length is None:
            # Accept blank → default
            raw = get_input(f"  Length ({MIN_LENGTH}–{MAX_LENGTH}) [default 16]: ")
            if raw == "":
                length = 16
                break
            print_error(f"Enter a number between {MIN_LENGTH} and {MAX_LENGTH}.")
            continue
        break

    # ── character categories ──────────────────────────────────
    print()
    print("  Select character types (press ENTER to accept default Y):")
    use_upper   = confirm("  Include Uppercase  (A-Z)?")
    use_lower   = confirm("  Include Lowercase  (a-z)?")
    use_digits  = confirm("  Include Digits     (0-9)?")
    use_symbols = confirm("  Include Symbols (!@#…)?")

    # ── validate ─────────────────────────────────────────────
    vr = validate_generation_request(length, use_upper, use_lower, use_digits, use_symbols)
    if not vr:
        for err in vr.errors:
            print_error(err)
        return None

    return PasswordConfig(
        length=length,
        use_upper=use_upper,
        use_lower=use_lower,
        use_digits=use_digits,
        use_symbols=use_symbols,
    )


# ──────────────────────────────────────────────────────────────
# Menu actions
# ──────────────────────────────────────────────────────────────


def action_generate_single() -> None:
    """Generate a single password, show its strength report, and offer to copy."""
    config = _collect_config()
    if config is None:
        return

    password = generate_password(config)
    report   = analyse(password)

    print(report.display())

    # Copy to clipboard
    if _CLIPBOARD_AVAILABLE:
        if confirm("Copy password to clipboard?"):
            if _copy_to_clipboard(password):
                print_success("Password copied to clipboard.")
            else:
                print_error("Clipboard copy failed.")
    else:
        print_info("Install pyperclip to enable clipboard support.")


def action_generate_bulk() -> None:
    """Generate multiple passwords and offer to save them to a file."""
    config = _collect_config()
    if config is None:
        return

    print()
    while True:
        count = get_int_input(
            f"  How many passwords to generate (1–{MAX_BULK})? ",
            min_val=1,
            max_val=MAX_BULK,
        )
        if count is None:
            print_error(f"Enter a number between 1 and {MAX_BULK}.")
            continue
        vr = validate_bulk_count(count)
        if not vr:
            print_error(vr.first_error or "Invalid count.")
            continue
        break

    passwords = generate_bulk(config, count)

    print()
    print_separator()
    print(f"  Generated {count} password(s):\n")
    for i, pw in enumerate(passwords, 1):
        print(f"  {i:>4}.  {pw}")
    print_separator()

    if confirm("Save passwords to a file?"):
        _save_passwords(passwords, config)


def action_export_passwords() -> None:
    """Generate and immediately export passwords to a TXT file."""
    config = _collect_config()
    if config is None:
        return

    print()
    while True:
        count = get_int_input(
            f"  How many passwords to export (1–{MAX_BULK})? ",
            min_val=1,
            max_val=MAX_BULK,
        )
        if count is None:
            print_error(f"Enter a number between 1 and {MAX_BULK}.")
            continue
        break

    passwords = generate_bulk(config, count)
    _save_passwords(passwords, config)


def _save_passwords(passwords: list[str], config: PasswordConfig) -> None:
    """
    Write a list of passwords to a timestamped TXT file.

    Args:
        passwords: List of password strings to save.
        config:    The config used to generate them (written to the header).
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_path = Path(f"passwords_{timestamp}.txt")

    raw = get_input(f"\n  File path [default: {default_path}]: ").strip()
    output_path = Path(raw) if raw else default_path

    # Build file content
    lines = [
        "=" * 56,
        "  Professional Password Generator — Export",
        f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Count     : {len(passwords)}",
        f"  Length    : {config.length}",
        f"  Uppercase : {'Yes' if config.use_upper   else 'No'}",
        f"  Lowercase : {'Yes' if config.use_lower   else 'No'}",
        f"  Digits    : {'Yes' if config.use_digits  else 'No'}",
        f"  Symbols   : {'Yes' if config.use_symbols else 'No'}",
        "=" * 56,
        "",
    ]
    for i, pw in enumerate(passwords, 1):
        lines.append(f"{i:>4}.  {pw}")

    lines += [
        "",
        "=" * 56,
        "  SECURITY NOTICE: Store this file in a secure location.",
        "  Delete it once passwords have been transferred to a",
        "  password manager.",
        "=" * 56,
    ]

    try:
        output_path.write_text("\n".join(lines), encoding="utf-8")
        print_success(f"Saved {len(passwords)} password(s) to: {output_path.resolve()}")
    except OSError as exc:
        print_error(f"Could not write file: {exc}")


# ──────────────────────────────────────────────────────────────
# Main menu
# ──────────────────────────────────────────────────────────────


def show_main_menu() -> None:
    """Render the main menu."""
    clear_screen()
    print_banner()
    print_separator()
    print("  MAIN MENU")
    print_separator()
    print("  [1]  Generate Password")
    print("  [2]  Bulk Generation")
    print("  [3]  Export Passwords to File")
    print_separator()
    print("  [Q]  Quit")
    print_separator()


def main() -> None:
    """Application entry point and main event loop."""
    while True:
        show_main_menu()
        choice = get_menu_choice("  Choose an option: ", {"1", "2", "3", "q"})

        if choice == "q":
            clear_screen()
            print_banner()
            print("\n  👋  Thank you for using Password Generator. Stay secure!\n")
            sys.exit(0)

        clear_screen()
        print_banner()

        if choice == "1":
            action_generate_single()
        elif choice == "2":
            action_generate_bulk()
        elif choice == "3":
            action_export_passwords()

        print()
        get_input("  Press ENTER to return to the menu…")


if __name__ == "__main__":
    main()

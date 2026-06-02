"""
main.py — Entry point for the Rock Paper Scissors CLI game.

Run with:
    python main.py
"""

import sys

# Ensure the project root is on the path so 'src' is importable
# regardless of where the user invokes the script from.
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import MODE_KEYS, MODE_LABELS, GameSession
from src.stats import Stats
from src.utils import (
    SEPARATOR,
    clear_screen,
    get_input,
    get_menu_choice,
    print_banner,
    print_separator,
)


# ──────────────────────────────────────────────────────────────
# Menu builders
# ──────────────────────────────────────────────────────────────


def show_main_menu() -> None:
    """Render the main menu to stdout."""
    clear_screen()
    print_banner()
    print_separator()
    print("  MAIN MENU")
    print_separator()
    print("  [1]  Single Round")
    print("  [2]  Best of 3")
    print("  [3]  Best of 5")
    print("  [4]  Unlimited Mode")
    print_separator()
    print("  [S]  View Overall Stats")
    print("  [Q]  Quit")
    print_separator()


def show_stats_screen(lifetime: Stats) -> None:
    """Display the lifetime statistics screen."""
    clear_screen()
    print_banner()
    print(lifetime.summary("Overall Lifetime Stats"))
    print()
    get_input("  Press ENTER to return to the menu…")


# ──────────────────────────────────────────────────────────────
# Application loop
# ──────────────────────────────────────────────────────────────


def main() -> None:
    """Main application loop."""
    lifetime_stats = Stats()

    while True:
        show_main_menu()
        choice = get_menu_choice(
            "  Choose an option: ", {"1", "2", "3", "4", "s", "q"}
        )

        if choice == "q":
            clear_screen()
            print_banner()
            print(lifetime_stats.summary("Final Lifetime Stats"))
            print("\n  👋  Thanks for playing! Goodbye.\n")
            sys.exit(0)

        if choice == "s":
            show_stats_screen(lifetime_stats)
            continue

        # ── start a game session ────────────────────────────
        mode = MODE_KEYS[choice]
        session = GameSession(mode)

        try:
            session_stats = session.play()
        except KeyboardInterrupt:
            print("\n\n  Game interrupted.\n")
            session_stats = session.session_stats

        # Merge session results into lifetime totals
        lifetime_stats.merge(session_stats)

        # ── play-again prompt ────────────────────────────────
        print()
        print_separator()
        again = get_menu_choice(
            "  Play again? [y] Yes  [n] No : ", {"y", "n"}
        )
        if again == "n":
            clear_screen()
            print_banner()
            print(lifetime_stats.summary("Final Lifetime Stats"))
            print("\n  👋  Thanks for playing! Goodbye.\n")
            sys.exit(0)


if __name__ == "__main__":
    main()

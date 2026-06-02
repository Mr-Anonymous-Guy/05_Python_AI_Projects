# ✊ 🖐 ✌ Rock Paper Scissors

A professional, terminal-based Rock Paper Scissors game built with pure Python.  
Part of the **05_Python_AI_Projects** repository — Project 01: Python Fundamentals.

---

## What You'll Learn

| Concept | Where it's used |
|---|---|
| Variables | `stats.py`, `game.py` — score tracking, state |
| Functions | Every module — small, single-purpose functions |
| Loops | `game.py` — round loop; `main.py` — menu loop |
| Conditionals | `game.py` — winner logic, mode checks |
| Input Validation | `utils.py` — `validate_choice()`, `get_menu_choice()` |
| Random Module | `player.py` — `ComputerPlayer.get_choice()` |
| Modular Programming | Entire `src/` package architecture |

---

## Features

### Game Modes
| Mode | Description |
|---|---|
| Single Round | One round, one result |
| Best of 3 | First to 2 wins |
| Best of 5 | First to 3 wins |
| Unlimited | Play until you choose to stop |

### Statistics
- Rounds played, wins, losses, draws
- Win-rate percentage
- Per-session stats and lifetime totals

### CLI
- Animated banner and clean console UI
- Numeric, letter, and full-word move input (`1`, `r`, `rock`)
- Input validation with helpful error messages
- Replay option and graceful exit

---

## Project Structure

```
Rock_Paper_Scissors/
├── src/
│   ├── __init__.py     # Package marker
│   ├── game.py         # Core logic: determine_winner(), GameSession
│   ├── player.py       # HumanPlayer & ComputerPlayer
│   ├── stats.py        # Stats dataclass (wins / losses / draws / win-rate)
│   └── utils.py        # Console UI, input validation, constants
│
├── tests/
│   ├── __init__.py
│   └── test_game.py    # 45 unit + integration tests
│
├── main.py             # CLI entry point
├── requirements.txt
├── run.sh              # Linux / macOS launcher
├── run.bat             # Windows launcher
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites
- Python **3.8** or newer
- No third-party packages needed to play

```bash
python --version   # should be 3.8+
```

### Run the game

**Linux / macOS**
```bash
chmod +x run.sh
./run.sh
```

**Windows**
```bat
run.bat
```

**Direct**
```bash
python main.py
```

---

## Running Tests

```bash
# Using pytest (recommended)
pip install pytest
python -m pytest tests/ -v

# Using built-in unittest (zero dependencies)
python -m unittest discover tests/ -v
```

Expected output:
```
tests/test_game.py::TestDetermineWinner::test_rock_beats_scissors  PASSED
tests/test_game.py::TestDetermineWinner::test_scissors_beats_paper PASSED
...
45 passed in 0.10s
```

---

## Example Terminal Output

```
╔══════════════════════════════════════════════════════╗
║        ✊ 🖐  ✌  ROCK  PAPER  SCISSORS  ✊ 🖐  ✌       ║
╚══════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────
  MAIN MENU
──────────────────────────────────────────────────────
  [1]  Single Round
  [2]  Best of 3
  [3]  Best of 5
  [4]  Unlimited Mode
──────────────────────────────────────────────────────
  [S]  View Overall Stats
  [Q]  Quit
──────────────────────────────────────────────────────
  Choose an option: 2

──────────────────────────────────────────────────────
  🎮  Mode: Best of 3
──────────────────────────────────────────────────────

  ────────────────────────────────────
  Round 1
  ────────────────────────────────────

  Your move → [1] Rock  [2] Paper  [3] Scissors : 1

  You             🪨  Rock
  Computer        ✂️  Scissors

  🏆  You win this round!

  Score →  You 1  :  0  Computer  (Draws: 0)

  ────────────────────────────────────
  Round 2
  ────────────────────────────────────

  Your move → [1] Rock  [2] Paper  [3] Scissors : r

  You             🪨  Rock
  Computer        🪨  Rock

  🤝  It's a draw!

  Score →  You 1  :  0  Computer  (Draws: 1)

  ────────────────────────────────────
  Round 3
  ────────────────────────────────────

  Your move → [1] Rock  [2] Paper  [3] Scissors : scissors

  You             ✂️  Scissors
  Computer        📄  Paper

  🏆  You win this round!

  Score →  You 2  :  0  Computer  (Draws: 1)

──────────────────────────────────────────────────────
  🏆  RESULT: YOU WIN THE MATCH!

  ────────────────────────────────────
  📊  Session Stats
  ────────────────────────────────────
  🎮  Rounds Played : 3
  ✅  Wins          : 2
  ❌  Losses        : 0
  🤝  Draws         : 1
  📈  Win Rate      : 66.7%
  ────────────────────────────────────

──────────────────────────────────────────────────────
  Play again? [y] Yes  [n] No : n

  Final Lifetime Stats
  🎮  Rounds Played : 3
  ✅  Wins          : 2  |  ❌  Losses : 0  |  🤝  Draws : 1
  📈  Win Rate      : 66.7%

  👋  Thanks for playing! Goodbye.
```

---

## Architecture Notes

### Separation of concerns
| Module | Responsibility |
|---|---|
| `utils.py` | All console I/O and input validation |
| `player.py` | Player abstractions (human & computer) |
| `stats.py` | Pure data — no I/O |
| `game.py` | Business logic — orchestrates a session |
| `main.py` | Application shell — menus and loops |

### Design principles
- **Small functions** — each function does one thing
- **Type hints** throughout for IDE support and readability  
- **Docstrings** on every public function and class
- **No global state** — stats are passed/returned explicitly
- **Crash-safe** — `KeyboardInterrupt` and `EOFError` are caught at the boundary

---

## License

MIT — free to use, fork, and learn from.

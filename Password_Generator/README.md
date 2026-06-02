# 🔐 Professional Password Generator

A cryptographically secure, terminal-based password generator built with pure Python.  
Part of the **05_Python_AI_Projects** repository — Project 02: Python Fundamentals.

---

## What You'll Learn

| Concept | Where it's demonstrated |
|---|---|
| String Manipulation | `generator.py` — charset building, `strength.py` — char analysis |
| Randomization | `generator.py` — `secrets.choice()` & `secrets.SystemRandom` |
| Security Concepts | CSPRNG vs PRNG, complexity rules, strength scoring |
| Input Validation | `validator.py` — length, charset, and bulk-count rules |
| File Handling | `main.py` — `pathlib.Path` for safe file export |
| Modular Programming | Entire `src/` package — one responsibility per module |

> **Security note:** This project uses Python's [`secrets`](https://docs.python.org/3/library/secrets.html) module — backed by the OS CSPRNG (`/dev/urandom` on Linux/macOS, `CryptGenRandom` on Windows) — rather than `random`, making passwords unpredictable even to an attacker who knows the time the program ran.

---

## Features

### Password Generation
| Option | Description |
|---|---|
| Custom length | 4 – 512 characters |
| Uppercase (A–Z) | Toggle on/off |
| Lowercase (a–z) | Toggle on/off |
| Digits (0–9) | Toggle on/off |
| Symbols (!@#…) | Toggle on/off |

At least one character from every enabled category is **guaranteed** to appear in the output.

### Strength Analysis
Every generated password is immediately scored against five weighted criteria:

| Criterion | Max pts |
|---|---|
| Length (log scale) | 40 |
| Uppercase chars | 10 |
| Lowercase chars | 10 |
| Digit chars | 10 |
| Symbol chars | 15 |
| Character variety | 15 |
| **Total** | **100** |

Rating thresholds: Very Weak · Weak · Fair · Strong · **Very Strong 💎**

### Productivity
- **Bulk generation** — generate 1 – 1,000 passwords in one shot
- **Clipboard copy** — one-key copy (requires optional `pyperclip`)
- **File export** — timestamped `.txt` export with config header and security notice

---

## Project Structure

```
Password_Generator/
├── src/
│   ├── __init__.py      # Package marker
│   ├── generator.py     # CSPRNG password generation engine
│   ├── validator.py     # Pure validation logic (no I/O)
│   ├── strength.py      # Password strength analyser
│   └── utils.py         # Console UI, prompts, and formatting
│
├── tests/
│   ├── __init__.py
│   ├── test_generator.py  # 20 tests — generation correctness
│   ├── test_validator.py  # 29 tests — input validation
│   └── test_strength.py   # 40 tests — strength scoring
│
├── main.py              # CLI entry point
├── requirements.txt
├── run.sh               # Linux / macOS launcher
├── run.bat              # Windows launcher
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites
- Python **3.8** or newer (uses `secrets` module and `dataclasses`)
- No third-party packages required for core functionality

```bash
python --version   # 3.8+
```

### Optional — clipboard support
```bash
pip install pyperclip
```

### Run the app

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
# pytest (recommended)
pip install pytest
python -m pytest tests/ -v

# Built-in unittest — zero dependencies
python -m unittest discover tests/ -v
```

Expected output:
```
89 passed, 18 subtests passed in 0.10s
```

---

## Example Terminal Output

```
╔══════════════════════════════════════════════════════╗
║            🔐  PROFESSIONAL PASSWORD GENERATOR        ║
╚══════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────
  MAIN MENU
──────────────────────────────────────────────────────
  [1]  Generate Password
  [2]  Bulk Generation
  [3]  Export Passwords to File
──────────────────────────────────────────────────────
  [Q]  Quit
──────────────────────────────────────────────────────
  Choose an option: 1

──────────────────────────────────────────────────────
  ⚙️   Password Configuration
──────────────────────────────────────────────────────
  Length (4–512) [default 16]: 20
  Include Uppercase  (A-Z)? [y/n]: y
  Include Lowercase  (a-z)? [y/n]: y
  Include Digits     (0-9)? [y/n]: y
  Include Symbols (!@#…)?  [y/n]: y

  ──────────────────────────────────────────
  📊  Password Analysis
  ──────────────────────────────────────────
  🔑  Password     : mK$7rZ!2pQv@8nLe#4Wj
  📏  Length       : 20 characters
  ──────────────────────────────────────────
  🔠  Uppercase    : 5
  🔡  Lowercase    : 8
  🔢  Digits       : 4
  🔣  Symbols      : 3
  🎲  Unique chars : 19
  🎨  Categories   : 4 / 4
  ──────────────────────────────────────────
  💎  Strength     : Very Strong  (94/100)
  ──────────────────────────────────────────

  Copy password to clipboard? [y/n]: y
  ✅  Password copied to clipboard.
```

### Bulk export example
```
  How many passwords to generate (1–1000)? 5

  Generated 5 password(s):

     1.  Xq#7mP2@kRn!4vLe
     2.  jB$9wZ!3nKr@6mQp
     3.  Yw!4pN7@xKm#2vRq
     4.  Lk$8rZ!5mQv@3nPx
     5.  Mp#6wN9@kRn!2vZj

  Save passwords to a file? [y/n]: y
  File path [default: passwords_20240602_143022.txt]:
  ✅  Saved 5 password(s) to: C:\...\passwords_20240602_143022.txt
```

---

## Architecture Notes

### Module responsibilities

| Module | Purpose |
|---|---|
| `generator.py` | CSPRNG generation only — no I/O, no validation |
| `validator.py` | Pure validation functions returning `ValidationResult` |
| `strength.py` | Pure analysis functions returning `StrengthReport` |
| `utils.py` | All console I/O — keeps other modules clean |
| `main.py` | Orchestration: menus, user flow, file I/O |

### Why `secrets` and not `random`?

`random` is a pseudo-random number generator (PRNG). Its output is deterministic given the seed — and the seed is often the system time, which is guessable. `secrets` reads from the OS CSPRNG, which sources entropy from hardware events, making the output statistically indistinguishable from true randomness.

### Guaranteed category inclusion

A naive `[secrets.choice(charset) for _ in range(n)]` loop can produce a password that omits an enabled category. This generator pre-picks one character per enabled category, fills the rest randomly from the full charset, then shuffles everything with `secrets.SystemRandom()` — so the mandatory characters never appear in predictable positions.

---

## License

MIT — free to use, fork, and learn from.

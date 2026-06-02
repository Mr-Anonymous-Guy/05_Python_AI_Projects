#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# run.sh — Launch Rock Paper Scissors on Linux / macOS
# ──────────────────────────────────────────────────────────────
set -euo pipefail

# Move to the directory that contains this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Python interpreter detection ──────────────────────────────
if command -v python3 &>/dev/null; then
    PY="python3"
elif command -v python &>/dev/null; then
    PY="python"
else
    echo "❌  Python not found. Please install Python 3.8 or newer."
    exit 1
fi

# ── Version guard ─────────────────────────────────────────────
PYVER=$("$PY" -c "import sys; print(sys.version_info.minor + sys.version_info.major * 10)")
if [ "$PYVER" -lt 38 ]; then
    echo "❌  Python 3.8+ is required. Found: $($PY --version)"
    exit 1
fi

echo "▶  Using $($PY --version)"
echo "▶  Starting Rock Paper Scissors…"
echo ""

"$PY" main.py

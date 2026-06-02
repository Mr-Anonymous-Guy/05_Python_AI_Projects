#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# run.sh — Launch AI Resume Builder on Linux / macOS
# ──────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════╗"
echo "║        AI RESUME BUILDER - Flask Application         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── Python detection ──────────────────────────────────────────
if command -v python3 &>/dev/null; then
    PY="python3"
elif command -v python &>/dev/null; then
    PY="python"
else
    echo "❌  Python not found. Please install Python 3.8+."
    exit 1
fi

echo "✓ Using $($PY --version)"

# ── Ollama check ──────────────────────────────────────────────
if ! command -v ollama &>/dev/null; then
    echo "⚠️  WARNING: Ollama not found."
    echo "   AI features require Ollama to be installed."
    echo "   Visit: https://ollama.ai"
    echo ""
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Ollama is installed"
    if ! pgrep -x "ollama" > /dev/null; then
        echo "⚠️  Ollama server is not running."
        echo "   Start with: ollama serve"
        echo ""
    fi
fi

# ── Dependencies ──────────────────────────────────────────────
if ! "$PY" -c "import flask" &>/dev/null; then
    echo ""
    echo "📦 Installing dependencies..."
    "$PY" -m pip install -r requirements.txt
fi

echo ""
echo "🚀 Starting Flask server..."
echo "   URL: http://localhost:5000"
echo "   Press CTRL+C to stop"
echo ""

"$PY" app.py

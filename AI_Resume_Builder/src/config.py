"""
config.py — Application configuration and constants.

Centralizes all settings for Ollama, Flask, file paths, and AI parameters.
"""

import os
from pathlib import Path
from typing import Final

# ──────────────────────────────────────────────────────────────
# Project paths
# ──────────────────────────────────────────────────────────────

PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent
APP_DIR: Final[Path] = PROJECT_ROOT / "app"
GENERATED_DIR: Final[Path] = PROJECT_ROOT / "generated"
PROMPTS_DIR: Final[Path] = PROJECT_ROOT / "prompts"
SRC_DIR: Final[Path] = PROJECT_ROOT / "src"

# Ensure directories exist
GENERATED_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)
APP_DIR.mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────────
# Ollama configuration
# ──────────────────────────────────────────────────────────────

OLLAMA_BASE_URL: Final[str] = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL: Final[str] = os.getenv("OLLAMA_MODEL", "llama3")

SUPPORTED_MODELS: Final[list[str]] = [
    "llama3",
    "llama3.1",
    "llama3.2",
    "mistral",
    "gemma",
    "gemma2",
    "qwen",
    "qwen2",
]

# Generation parameters
TEMPERATURE: Final[float] = 0.7
MAX_TOKENS: Final[int] = 2048
TOP_P: Final[float] = 0.9

# ──────────────────────────────────────────────────────────────
# Flask configuration
# ──────────────────────────────────────────────────────────────

FLASK_HOST: Final[str] = "0.0.0.0"
FLASK_PORT: Final[int] = 5000
FLASK_DEBUG: Final[bool] = os.getenv("FLASK_DEBUG", "False").lower() == "true"
SECRET_KEY: Final[str] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# ──────────────────────────────────────────────────────────────
# ATS scoring weights
# ──────────────────────────────────────────────────────────────

ATS_WEIGHTS: Final[dict[str, float]] = {
    "keywords": 0.30,
    "formatting": 0.20,
    "experience": 0.25,
    "skills": 0.15,
    "education": 0.10,
}

# Minimum score thresholds
ATS_SCORE_EXCELLENT: Final[int] = 80
ATS_SCORE_GOOD: Final[int] = 60
ATS_SCORE_FAIR: Final[int] = 40

# ──────────────────────────────────────────────────────────────
# Export settings
# ──────────────────────────────────────────────────────────────

PDF_PAGE_SIZE: Final[str] = "LETTER"  # or "A4"
PDF_MARGIN_INCH: Final[float] = 0.75

DOCX_FONT_NAME: Final[str] = "Calibri"
DOCX_FONT_SIZE_BODY: Final[int] = 11
DOCX_FONT_SIZE_HEADING: Final[int] = 14

# ──────────────────────────────────────────────────────────────
# Logging configuration
# ──────────────────────────────────────────────────────────────

LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

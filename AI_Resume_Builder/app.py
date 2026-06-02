"""
app.py — Flask application for AI Resume Builder.

Provides REST API and web interface for resume generation,
ATS analysis, and document export.
"""

import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from src.ai_service import AIService
from src.ats_analyzer import analyze_resume
from src.config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT, GENERATED_DIR, SECRET_KEY
from src.exporters import export_to_docx, export_to_pdf, export_to_txt
from src.models import (
    Certification,
    Education,
    Experience,
    PersonalInfo,
    Project,
    Resume,
)
from src.ollama_client import OllamaClient, OllamaConnectionError

# ──────────────────────────────────────────────────────────────
# App setup
# ──────────────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize services
ollama_client = OllamaClient()
ai_service = AIService(ollama_client)


# ──────────────────────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────────────────────


@app.route("/")
def index():
    """Serve main application page."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    ollama_status = ollama_client.check_health()
    return jsonify({
        "status": "healthy" if ollama_status else "degraded",
        "ollama": "connected" if ollama_status else "disconnected",
        "timestamp": datetime.now().isoformat(),
    })


# ──────────────────────────────────────────────────────────────
# AI generation endpoints
# ──────────────────────────────────────────────────────────────


@app.route("/api/generate/summary", methods=["POST"])
def generate_summary():
    """Generate professional summary."""
    try:
        data = request.json
        summary = ai_service.generate_professional_summary(
            name=data["name"],
            target_role=data["target_role"],
            years_experience=data["years_experience"],
            skills=data["skills"],
            achievements=data.get("achievements", []),
        )
        return jsonify({"success": True, "summary": summary})
    except Exception as exc:
        logger.error(f"Summary generation failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/generate/cover-letter", methods=["POST"])
def generate_cover_letter():
    """Generate cover letter."""
    try:
        data = request.json
        letter = ai_service.generate_cover_letter(
            name=data["name"],
            position=data["position"],
            company=data["company"],
            job_description=data["job_description"],
            skills=data["skills"],
            experience_summary=data["experience_summary"],
            achievements=data.get("achievements", []),
        )
        return jsonify({"success": True, "cover_letter": letter})
    except Exception as exc:
        logger.error(f"Cover letter generation failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/generate/linkedin-about", methods=["POST"])
def generate_linkedin():
    """Generate LinkedIn About section."""
    try:
        data = request.json
        about = ai_service.generate_linkedin_about(
            name=data["name"],
            title=data["title"],
            industry=data["industry"],
            years_experience=data["years_experience"],
            skills=data["skills"],
            achievements=data.get("achievements", []),
            career_goals=data.get("career_goals", ""),
        )
        return jsonify({"success": True, "about": about})
    except Exception as exc:
        logger.error(f"LinkedIn about generation failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


# ──────────────────────────────────────────────────────────────
# ATS analysis
# ──────────────────────────────────────────────────────────────


@app.route("/api/analyze/ats", methods=["POST"])
def analyze_ats():
    """Analyze resume for ATS compatibility."""
    try:
        data = request.json
        resume = Resume.from_dict(data["resume"])
        job_description = data.get("job_description", "")

        result = analyze_resume(resume, job_description)
        return jsonify({"success": True, "result": result.to_dict()})
    except Exception as exc:
        logger.error(f"ATS analysis failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


# ──────────────────────────────────────────────────────────────
# Export endpoints
# ──────────────────────────────────────────────────────────────


@app.route("/api/export/pdf", methods=["POST"])
def export_pdf():
    """Export resume to PDF."""
    try:
        data = request.json
        resume = Resume.from_dict(data["resume"])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.pdf"
        output_path = GENERATED_DIR / filename

        export_to_pdf(resume, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception as exc:
        logger.error(f"PDF export failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/export/docx", methods=["POST"])
def export_docx():
    """Export resume to DOCX."""
    try:
        data = request.json
        resume = Resume.from_dict(data["resume"])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.docx"
        output_path = GENERATED_DIR / filename

        export_to_docx(resume, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception as exc:
        logger.error(f"DOCX export failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/export/txt", methods=["POST"])
def export_txt():
    """Export resume to TXT."""
    try:
        data = request.json
        resume = Resume.from_dict(data["resume"])

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{timestamp}.txt"
        output_path = GENERATED_DIR / filename

        export_to_txt(resume, output_path)
        return send_file(output_path, as_attachment=True, download_name=filename)
    except Exception as exc:
        logger.error(f"TXT export failed: {exc}")
        return jsonify({"success": False, "error": str(exc)}), 500


# ──────────────────────────────────────────────────────────────
# Error handlers
# ──────────────────────────────────────────────────────────────


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────


if __name__ == "__main__":
    logger.info(f"Starting AI Resume Builder on {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)

"""
ai_service.py — High-level AI service for resume generation tasks.

Orchestrates Ollama client with prompt templates for all AI features.
"""

import logging
from pathlib import Path
from typing import Optional

from src.config import PROMPTS_DIR
from src.models import Resume
from src.ollama_client import OllamaClient, OllamaConnectionError

logger = logging.getLogger(__name__)


class AIService:
    """High-level service for AI-powered resume features."""

    def __init__(self, client: Optional[OllamaClient] = None) -> None:
        """
        Initialize AI service.

        Args:
            client: Ollama client instance (creates new if None).
        """
        self.client = client or OllamaClient()

    def _load_prompt_template(self, template_name: str) -> str:
        """Load a prompt template from disk."""
        template_path = PROMPTS_DIR / f"{template_name}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {template_path}")
        return template_path.read_text(encoding="utf-8")

    def generate_professional_summary(
        self,
        name: str,
        target_role: str,
        years_experience: str,
        skills: list[str],
        achievements: list[str],
    ) -> str:
        """
        Generate an ATS-optimized professional summary.

        Args:
            name: Full name.
            target_role: Desired position.
            years_experience: E.g., "5+ years".
            skills: List of key skills.
            achievements: List of notable achievements.

        Returns:
            Generated summary text.
        """
        template = self._load_prompt_template("resume_summary")
        prompt = template.format(
            name=name,
            target_role=target_role,
            years_experience=years_experience,
            skills=", ".join(skills[:10]),
            achievements="; ".join(achievements[:3]),
        )

        try:
            return self.client.generate(prompt)
        except OllamaConnectionError as exc:
            logger.error(f"Failed to generate summary: {exc}")
            raise

    def generate_cover_letter(
        self,
        name: str,
        position: str,
        company: str,
        job_description: str,
        skills: list[str],
        experience_summary: str,
        achievements: list[str],
    ) -> str:
        """
        Generate a tailored cover letter.

        Args:
            name: Applicant name.
            position: Target position.
            company: Company name.
            job_description: Full job posting text.
            skills: Key skills.
            experience_summary: Brief experience overview.
            achievements: Notable achievements.

        Returns:
            Generated cover letter.
        """
        template = self._load_prompt_template("cover_letter")
        prompt = template.format(
            name=name,
            position=position,
            company=company,
            job_description=job_description[:1000],  # Truncate
            skills=", ".join(skills[:15]),
            experience_summary=experience_summary,
            achievements="; ".join(achievements[:5]),
        )

        return self.client.generate(prompt, max_tokens=1500)

    def generate_linkedin_about(
        self,
        name: str,
        title: str,
        industry: str,
        years_experience: str,
        skills: list[str],
        achievements: list[str],
        career_goals: str,
    ) -> str:
        """
        Generate LinkedIn About section.

        Args:
            name: Full name.
            title: Professional title.
            industry: Industry/domain.
            years_experience: Years in field.
            skills: Core competencies.
            achievements: Key achievements.
            career_goals: Career aspirations.

        Returns:
            Generated About section.
        """
        template = self._load_prompt_template("linkedin_about")
        prompt = template.format(
            name=name,
            title=title,
            industry=industry,
            years_experience=years_experience,
            skills=", ".join(skills[:12]),
            achievements="; ".join(achievements[:4]),
            career_goals=career_goals,
        )

        return self.client.generate(prompt, max_tokens=800)

    def tailor_resume_for_job(
        self,
        job_description: str,
        current_skills: list[str],
        experience_highlights: list[str],
    ) -> str:
        """
        Provide recommendations to tailor resume for a specific job.

        Args:
            job_description: Target job posting.
            current_skills: Current resume skills.
            experience_highlights: Key experience bullets.

        Returns:
            Structured recommendations.
        """
        template = self._load_prompt_template("tailor_resume")
        prompt = template.format(
            job_description=job_description[:1500],
            current_skills=", ".join(current_skills),
            experience_highlights="\n".join(experience_highlights[:8]),
        )

        return self.client.generate(prompt, max_tokens=1200)

"""
models.py — Data models for resume components.

Uses dataclasses for type safety and automatic serialization.
All models support dict conversion for JSON API responses.
"""

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any, Optional


# ──────────────────────────────────────────────────────────────
# Personal Information
# ──────────────────────────────────────────────────────────────


@dataclass
class PersonalInfo:
    """Personal and contact information."""

    full_name: str
    email: str
    phone: str
    location: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────────────────────
# Education
# ──────────────────────────────────────────────────────────────


@dataclass
class Education:
    """Educational qualification."""

    institution: str
    degree: str
    field: str
    start_date: str  # YYYY-MM format
    end_date: str  # YYYY-MM or "Present"
    gpa: Optional[str] = None
    achievements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────────────────────
# Experience
# ──────────────────────────────────────────────────────────────


@dataclass
class Experience:
    """Work experience entry."""

    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    responsibilities: list[str] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────────────────────
# Project
# ──────────────────────────────────────────────────────────────


@dataclass
class Project:
    """Project entry."""

    title: str
    description: str
    technologies: list[str] = field(default_factory=list)
    link: Optional[str] = None
    highlights: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────────────────────
# Certification
# ──────────────────────────────────────────────────────────────


@dataclass
class Certification:
    """Professional certification."""

    name: str
    issuer: str
    date: str
    credential_id: Optional[str] = None
    link: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ──────────────────────────────────────────────────────────────
# Complete Resume
# ──────────────────────────────────────────────────────────────


@dataclass
class Resume:
    """
    Complete resume data model.

    This is the central data structure that all other components
    (AI generation, ATS analysis, export) operate on.
    """

    personal_info: PersonalInfo
    education: list[Education] = field(default_factory=list)
    experience: list[Experience] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    certifications: list[Certification] = field(default_factory=list)
    achievements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to a JSON-serializable dictionary."""
        return {
            "personal_info": self.personal_info.to_dict(),
            "education": [e.to_dict() for e in self.education],
            "experience": [e.to_dict() for e in self.experience],
            "skills": self.skills,
            "projects": [p.to_dict() for p in self.projects],
            "certifications": [c.to_dict() for c in self.certifications],
            "achievements": self.achievements,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Resume":
        """Reconstruct a Resume from a dictionary."""
        return cls(
            personal_info=PersonalInfo(**data["personal_info"]),
            education=[Education(**e) for e in data.get("education", [])],
            experience=[Experience(**e) for e in data.get("experience", [])],
            skills=data.get("skills", []),
            projects=[Project(**p) for p in data.get("projects", [])],
            certifications=[Certification(**c) for c in data.get("certifications", [])],
            achievements=data.get("achievements", []),
        )


# ──────────────────────────────────────────────────────────────
# ATS Analysis Result
# ──────────────────────────────────────────────────────────────


@dataclass
class ATSResult:
    """ATS analysis result with score and recommendations."""

    score: int  # 0-100
    rating: str  # "Excellent", "Good", "Fair", "Poor"
    keywords_found: list[str]
    keywords_missing: list[str]
    recommendations: list[str]
    strengths: list[str]
    weaknesses: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

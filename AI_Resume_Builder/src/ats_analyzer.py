"""
ats_analyzer.py — ATS (Applicant Tracking System) scoring engine.

Analyzes resumes against job descriptions and industry standards,
providing a score, keyword analysis, and actionable recommendations.
"""

import logging
import re
from typing import Any

from src.config import (
    ATS_SCORE_EXCELLENT,
    ATS_SCORE_FAIR,
    ATS_SCORE_GOOD,
    ATS_WEIGHTS,
)
from src.models import ATSResult, Resume

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Keyword extraction
# ──────────────────────────────────────────────────────────────


def extract_keywords(text: str) -> set[str]:
    """
    Extract potential keywords from text.

    Args:
        text: Input text (job description or resume content).

    Returns:
        Set of normalized keywords (lowercase, alphanumeric).
    """
    # Remove special characters, lowercase, split
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#\.]*\b', text.lower())

    # Filter out common stopwords
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "by", "from", "as", "is", "was", "are",
        "be", "have", "has", "had", "do", "does", "did", "will", "would",
        "should", "could", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they",
    }

    keywords = {w for w in words if len(w) > 2 and w not in stopwords}
    return keywords


def extract_skills_from_text(text: str) -> set[str]:
    """
    Extract technical skills and tools from text.

    Returns:
        Set of identified skills.
    """
    # Common skill patterns
    skill_patterns = [
        r'\b[A-Z][a-zA-Z]+(?:\.[a-z]+)+\b',  # e.g., React.js, Node.js
        r'\b[A-Z]{2,}\b',  # Acronyms: AWS, GCP, ML
        r'\b[A-Z][a-z]+\+\+\b',  # C++
        r'\b[A-Z][a-z]+#\b',  # C#, F#
    ]

    skills = set()
    for pattern in skill_patterns:
        skills.update(re.findall(pattern, text))

    return skills


# ──────────────────────────────────────────────────────────────
# Scoring components
# ──────────────────────────────────────────────────────────────


def score_keywords(
    resume: Resume,
    job_description: str,
) -> tuple[float, list[str], list[str]]:
    """
    Score keyword matching between resume and job description.

    Args:
        resume: Resume data.
        job_description: Target job description text.

    Returns:
        (score_0_to_100, found_keywords, missing_keywords)
    """
    # Extract keywords from job description
    jd_keywords = extract_keywords(job_description)

    # Extract keywords from resume
    resume_text = " ".join([
        resume.personal_info.summary or "",
        " ".join(resume.skills),
        " ".join([e.position for e in resume.experience]),
        " ".join([e.field for e in resume.education]),
    ])
    resume_keywords = extract_keywords(resume_text)

    # Calculate match
    if not jd_keywords:
        return 100.0, [], []

    found = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords

    # Score based on coverage
    coverage = len(found) / len(jd_keywords)
    score = coverage * 100

    return score, sorted(found)[:20], sorted(missing)[:20]


def score_formatting(resume: Resume) -> float:
    """
    Score resume formatting and structure.

    Checks for:
    - Clear contact information
    - Professional sections
    - Proper date formats
    - Quantifiable achievements

    Returns:
        Score from 0 to 100.
    """
    score = 0.0

    # Contact info completeness (20 points)
    pi = resume.personal_info
    if pi.email and pi.phone:
        score += 20

    # Required sections (20 points each)
    if resume.education:
        score += 20
    if resume.experience:
        score += 20
    if resume.skills:
        score += 20

    # Professional links (10 points)
    if pi.linkedin or pi.github or pi.portfolio:
        score += 10

    # Quantifiable achievements (10 points)
    has_numbers = False
    for exp in resume.experience:
        for item in exp.responsibilities + exp.achievements:
            if re.search(r'\d+%?|\$[\d,]+', item):
                has_numbers = True
                break
    if has_numbers:
        score += 10

    return min(score, 100.0)


def score_experience(resume: Resume) -> float:
    """
    Score experience section quality.

    Returns:
        Score from 0 to 100.
    """
    if not resume.experience:
        return 0.0

    score = 0.0

    # Number of experiences (30 points)
    num_exp = len(resume.experience)
    if num_exp >= 3:
        score += 30
    elif num_exp == 2:
        score += 20
    elif num_exp == 1:
        score += 10

    # Responsibilities/achievements detail (40 points)
    total_items = sum(
        len(e.responsibilities) + len(e.achievements)
        for e in resume.experience
    )
    if total_items >= 12:
        score += 40
    elif total_items >= 6:
        score += 25
    elif total_items >= 3:
        score += 15

    # Action verbs (30 points)
    action_verbs = {
        "led", "managed", "developed", "created", "implemented",
        "designed", "optimized", "improved", "increased", "reduced",
        "launched", "built", "achieved", "delivered", "coordinated",
    }
    verb_count = 0
    for exp in resume.experience:
        for item in exp.responsibilities + exp.achievements:
            first_word = item.split()[0].lower() if item else ""
            if first_word in action_verbs:
                verb_count += 1

    if verb_count >= 5:
        score += 30
    elif verb_count >= 3:
        score += 20
    elif verb_count >= 1:
        score += 10

    return min(score, 100.0)


def score_skills(resume: Resume, job_description: str) -> float:
    """
    Score skills section relevance and completeness.

    Returns:
        Score from 0 to 100.
    """
    if not resume.skills:
        return 0.0

    score = 0.0

    # Number of skills (40 points)
    num_skills = len(resume.skills)
    if num_skills >= 10:
        score += 40
    elif num_skills >= 6:
        score += 30
    elif num_skills >= 3:
        score += 20

    # Skill categorization (30 points)
    # Award points for having a mix of technical and soft skills
    technical_indicators = {"python", "java", "aws", "sql", "react", "docker"}
    soft_indicators = {"leadership", "communication", "teamwork", "problem"}

    has_technical = any(
        any(ind in skill.lower() for ind in technical_indicators)
        for skill in resume.skills
    )
    has_soft = any(
        any(ind in skill.lower() for ind in soft_indicators)
        for skill in resume.skills
    )

    if has_technical and has_soft:
        score += 30
    elif has_technical or has_soft:
        score += 15

    # Job description keyword match (30 points)
    jd_keywords = extract_keywords(job_description)
    skill_keywords = {kw.lower() for skill in resume.skills for kw in skill.split()}
    matches = skill_keywords & jd_keywords

    if job_description:
        match_ratio = len(matches) / max(len(jd_keywords), 1)
        score += match_ratio * 30

    return min(score, 100.0)


def score_education(resume: Resume) -> float:
    """
    Score education section.

    Returns:
        Score from 0 to 100.
    """
    if not resume.education:
        return 50.0  # Not critical if candidate has experience

    score = 0.0

    # Has degree (60 points)
    score += 60

    # GPA listed (20 points)
    if any(e.gpa for e in resume.education):
        score += 20

    # Achievements listed (20 points)
    if any(e.achievements for e in resume.education):
        score += 20

    return min(score, 100.0)


# ──────────────────────────────────────────────────────────────
# Main analyzer
# ──────────────────────────────────────────────────────────────


def analyze_resume(
    resume: Resume,
    job_description: str = "",
) -> ATSResult:
    """
    Comprehensive ATS analysis of a resume.

    Args:
        resume: Resume data to analyze.
        job_description: Optional job description for keyword matching.

    Returns:
        ATSResult with score and detailed feedback.
    """
    logger.info("Running ATS analysis...")

    # Compute component scores
    keyword_score, found_kw, missing_kw = score_keywords(resume, job_description)
    formatting_score = score_formatting(resume)
    experience_score = score_experience(resume)
    skills_score = score_skills(resume, job_description)
    education_score = score_education(resume)

    # Weighted final score
    final_score = (
        ATS_WEIGHTS["keywords"] * keyword_score +
        ATS_WEIGHTS["formatting"] * formatting_score +
        ATS_WEIGHTS["experience"] * experience_score +
        ATS_WEIGHTS["skills"] * skills_score +
        ATS_WEIGHTS["education"] * education_score
    )
    final_score = int(round(final_score))

    # Rating
    if final_score >= ATS_SCORE_EXCELLENT:
        rating = "Excellent"
    elif final_score >= ATS_SCORE_GOOD:
        rating = "Good"
    elif final_score >= ATS_SCORE_FAIR:
        rating = "Fair"
    else:
        rating = "Poor"

    # Generate recommendations
    recommendations = _generate_recommendations(
        resume, keyword_score, formatting_score,
        experience_score, skills_score, education_score
    )

    # Strengths and weaknesses
    strengths, weaknesses = _identify_strengths_weaknesses(
        keyword_score, formatting_score, experience_score,
        skills_score, education_score
    )

    return ATSResult(
        score=final_score,
        rating=rating,
        keywords_found=found_kw,
        keywords_missing=missing_kw,
        recommendations=recommendations,
        strengths=strengths,
        weaknesses=weaknesses,
    )


def _generate_recommendations(
    resume: Resume,
    kw_score: float,
    fmt_score: float,
    exp_score: float,
    skill_score: float,
    edu_score: float,
) -> list[str]:
    """Generate actionable recommendations based on component scores."""
    recs = []

    if kw_score < 60:
        recs.append("Add more keywords from the job description to your resume")
    if fmt_score < 70:
        recs.append("Improve resume structure with clear section headings")
    if exp_score < 70:
        recs.append("Add more quantifiable achievements to experience bullets")
        recs.append("Use strong action verbs to start each bullet point")
    if skill_score < 60:
        recs.append("Expand your skills section with relevant technical skills")
    if not resume.personal_info.linkedin:
        recs.append("Add a LinkedIn profile URL to increase credibility")
    if not resume.projects:
        recs.append("Include 2-3 relevant projects to demonstrate hands-on experience")

    return recs[:6]  # Top 6 recommendations


def _identify_strengths_weaknesses(
    kw_score: float,
    fmt_score: float,
    exp_score: float,
    skill_score: float,
    edu_score: float,
) -> tuple[list[str], list[str]]:
    """Identify top strengths and weaknesses."""
    scores = {
        "Keyword matching": kw_score,
        "Formatting": fmt_score,
        "Experience quality": exp_score,
        "Skills relevance": skill_score,
        "Education details": edu_score,
    }

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    strengths = [name for name, score in sorted_scores[:2] if score >= 70]
    weaknesses = [name for name, score in sorted_scores[-2:] if score < 70]

    return strengths, weaknesses

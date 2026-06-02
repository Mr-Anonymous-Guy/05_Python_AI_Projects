"""
test_ats_analyzer.py — Unit tests for ATS scoring engine.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ats_analyzer import (
    analyze_resume,
    extract_keywords,
    score_education,
    score_experience,
    score_formatting,
    score_keywords,
    score_skills,
)
from src.models import Education, Experience, PersonalInfo, Resume


class TestKeywordExtraction(unittest.TestCase):
    """Tests for keyword extraction."""

    def test_extract_basic_keywords(self) -> None:
        text = "Python Developer with experience in Django and Flask"
        keywords = extract_keywords(text)
        self.assertIn("python", keywords)
        self.assertIn("django", keywords)
        self.assertIn("flask", keywords)

    def test_filters_stopwords(self) -> None:
        text = "The developer and the engineer"
        keywords = extract_keywords(text)
        self.assertNotIn("the", keywords)
        self.assertNotIn("and", keywords)

    def test_handles_empty_string(self) -> None:
        keywords = extract_keywords("")
        self.assertEqual(keywords, set())


class TestScoring(unittest.TestCase):
    """Tests for individual scoring functions."""

    def setUp(self) -> None:
        self.resume = Resume(
            personal_info=PersonalInfo(
                full_name="John Doe",
                email="john@example.com",
                phone="555-0100",
                location="New York, NY",
                linkedin="linkedin.com/in/johndoe",
                summary="Experienced software engineer",
            ),
            skills=["Python", "JavaScript", "React", "AWS", "Docker"],
            experience=[
                Experience(
                    company="Tech Corp",
                    position="Senior Developer",
                    location="New York, NY",
                    start_date="2020-01",
                    end_date="Present",
                    responsibilities=[
                        "Led team of 5 developers",
                        "Improved performance by 40%",
                    ],
                    achievements=["Reduced costs by $50K annually"],
                )
            ],
            education=[
                Education(
                    institution="University",
                    degree="BS",
                    field="Computer Science",
                    start_date="2015-09",
                    end_date="2019-05",
                    gpa="3.8",
                )
            ],
        )

    def test_score_formatting(self) -> None:
        score = score_formatting(self.resume)
        self.assertGreater(score, 50)  # Should have decent formatting

    def test_score_experience(self) -> None:
        score = score_experience(self.resume)
        self.assertGreater(score, 0)

    def test_score_experience_empty(self) -> None:
        empty_resume = Resume(
            personal_info=PersonalInfo("", "", "", ""),
            experience=[],
        )
        score = score_experience(empty_resume)
        self.assertEqual(score, 0.0)

    def test_score_skills(self) -> None:
        score = score_skills(self.resume, "Python JavaScript AWS")
        self.assertGreater(score, 0)

    def test_score_education(self) -> None:
        score = score_education(self.resume)
        self.assertGreater(score, 50)


class TestATSAnalysis(unittest.TestCase):
    """Tests for complete ATS analysis."""

    def test_analyze_resume_basic(self) -> None:
        resume = Resume(
            personal_info=PersonalInfo(
                full_name="Jane Smith",
                email="jane@example.com",
                phone="555-0200",
                location="San Francisco, CA",
            ),
            skills=["Python", "Machine Learning", "TensorFlow"],
            experience=[
                Experience(
                    company="AI Startup",
                    position="ML Engineer",
                    location="SF",
                    start_date="2021-01",
                    end_date="Present",
                    responsibilities=["Built ML models"],
                )
            ],
            education=[
                Education(
                    institution="Stanford",
                    degree="MS",
                    field="AI",
                    start_date="2019",
                    end_date="2021",
                )
            ],
        )

        result = analyze_resume(resume, "Python Machine Learning Engineer")
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)
        self.assertIn(result.rating, ["Excellent", "Good", "Fair", "Poor"])
        self.assertIsInstance(result.recommendations, list)

    def test_analyze_minimal_resume(self) -> None:
        minimal = Resume(
            personal_info=PersonalInfo("", "", "", ""),
        )
        result = analyze_resume(minimal, "")
        self.assertLess(result.score, 50)  # Should score poorly


if __name__ == "__main__":
    unittest.main(verbosity=2)

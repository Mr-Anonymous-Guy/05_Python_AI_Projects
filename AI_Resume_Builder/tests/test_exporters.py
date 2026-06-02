"""
test_exporters.py — Unit tests for PDF, DOCX, and TXT exporters.
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.exporters import export_to_docx, export_to_pdf, export_to_txt
from src.models import Education, Experience, PersonalInfo, Project, Resume


class TestExporters(unittest.TestCase):
    """Tests for resume export functionality."""

    def setUp(self) -> None:
        """Create a sample resume for testing."""
        self.resume = Resume(
            personal_info=PersonalInfo(
                full_name="Test User",
                email="test@example.com",
                phone="555-0100",
                location="Test City, TS",
                linkedin="linkedin.com/in/testuser",
                github="github.com/testuser",
                summary="Test summary for resume export testing.",
            ),
            skills=["Python", "JavaScript", "AWS", "Docker"],
            experience=[
                Experience(
                    company="Test Company",
                    position="Software Engineer",
                    location="Test City",
                    start_date="2020-01",
                    end_date="Present",
                    responsibilities=[
                        "Developed backend services",
                        "Implemented CI/CD pipelines",
                    ],
                    achievements=["Improved performance by 40%"],
                )
            ],
            education=[
                Education(
                    institution="Test University",
                    degree="BS",
                    field="Computer Science",
                    start_date="2016-09",
                    end_date="2020-05",
                    gpa="3.8",
                )
            ],
            projects=[
                Project(
                    title="Test Project",
                    description="A test project for demonstration",
                    technologies=["Python", "Flask"],
                )
            ],
        )
        self.temp_dir = tempfile.mkdtemp()

    def test_export_to_pdf(self) -> None:
        """Test PDF export creates a file."""
        output_path = Path(self.temp_dir) / "test_resume.pdf"
        export_to_pdf(self.resume, output_path)

        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_export_to_docx(self) -> None:
        """Test DOCX export creates a file."""
        output_path = Path(self.temp_dir) / "test_resume.docx"
        export_to_docx(self.resume, output_path)

        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_export_to_txt(self) -> None:
        """Test TXT export creates a file."""
        output_path = Path(self.temp_dir) / "test_resume.txt"
        export_to_txt(self.resume, output_path)

        self.assertTrue(output_path.exists())
        content = output_path.read_text(encoding="utf-8")
        self.assertIn("Test User", content)
        self.assertIn("test@example.com", content)
        self.assertIn("Software Engineer", content)

    def test_txt_export_contains_all_sections(self) -> None:
        """Test TXT export includes all resume sections."""
        output_path = Path(self.temp_dir) / "test_resume_full.txt"
        export_to_txt(self.resume, output_path)

        content = output_path.read_text(encoding="utf-8")
        self.assertIn("PROFESSIONAL SUMMARY", content)
        self.assertIn("EXPERIENCE", content)
        self.assertIn("EDUCATION", content)
        self.assertIn("SKILLS", content)
        self.assertIn("PROJECTS", content)

    def test_export_minimal_resume(self) -> None:
        """Test exporting a minimal resume without errors."""
        minimal = Resume(
            personal_info=PersonalInfo(
                full_name="Minimal User",
                email="minimal@example.com",
                phone="555-0000",
                location="City",
            )
        )

        pdf_path = Path(self.temp_dir) / "minimal.pdf"
        docx_path = Path(self.temp_dir) / "minimal.docx"
        txt_path = Path(self.temp_dir) / "minimal.txt"

        # Should not raise exceptions
        export_to_pdf(minimal, pdf_path)
        export_to_docx(minimal, docx_path)
        export_to_txt(minimal, txt_path)

        self.assertTrue(pdf_path.exists())
        self.assertTrue(docx_path.exists())
        self.assertTrue(txt_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

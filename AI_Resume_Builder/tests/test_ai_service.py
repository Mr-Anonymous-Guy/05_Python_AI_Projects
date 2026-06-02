"""
test_ai_service.py — Unit tests for prompt loading and generation logic.
"""

import sys
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ai_service import AIService
from src.ollama_client import OllamaConnectionError


class TestAIService(unittest.TestCase):
    """Tests for the AI Service layer."""

    def setUp(self) -> None:
        # Mock the OllamaClient to prevent actual network calls
        self.mock_client = MagicMock()
        self.mock_client.generate.return_value = "Mocked generated response"
        self.ai_service = AIService(client=self.mock_client)

    @patch("src.ai_service.Path.read_text")
    @patch("src.ai_service.Path.exists")
    def test_load_prompt_template_success(self, mock_exists: MagicMock, mock_read_text: MagicMock) -> None:
        mock_exists.return_value = True
        mock_read_text.return_value = "Test template {name}"
        
        # Test loading a template
        content = self.ai_service._load_prompt_template("test_template")
        self.assertEqual(content, "Test template {name}")

    @patch("src.ai_service.Path.exists")
    def test_load_prompt_template_not_found(self, mock_exists: MagicMock) -> None:
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            self.ai_service._load_prompt_template("missing_template")

    @patch("src.ai_service.AIService._load_prompt_template")
    def test_generate_professional_summary(self, mock_load: MagicMock) -> None:
        # Provide a mock template string
        mock_load.return_value = "Summary for {name} ({target_role}, {years_experience}). Skills: {skills}. Achievements: {achievements}"
        
        result = self.ai_service.generate_professional_summary(
            name="Alice",
            target_role="Data Scientist",
            years_experience="3 years",
            skills=["Python", "SQL"],
            achievements=["Built ML model", "Improved revenue"]
        )
        
        self.assertEqual(result, "Mocked generated response")
        # Ensure the prompt was formatted properly and passed to the client
        self.mock_client.generate.assert_called_once()
        prompt_arg = self.mock_client.generate.call_args[0][0]
        self.assertIn("Alice", prompt_arg)
        self.assertIn("Data Scientist", prompt_arg)
        self.assertIn("Built ML model", prompt_arg)

    @patch("src.ai_service.AIService._load_prompt_template")
    def test_generate_cover_letter(self, mock_load: MagicMock) -> None:
        mock_load.return_value = "Cover letter for {name} applying to {company}."
        
        result = self.ai_service.generate_cover_letter(
            name="Bob",
            position="Backend Dev",
            company="Acme Corp",
            job_description="Need a developer",
            skills=["Go"],
            experience_summary="Backend experience",
            achievements=[]
        )
        
        self.assertEqual(result, "Mocked generated response")
        prompt_arg = self.mock_client.generate.call_args[0][0]
        self.assertIn("Bob", prompt_arg)
        self.assertIn("Acme Corp", prompt_arg)

    @patch("src.ai_service.AIService._load_prompt_template")
    def test_ai_service_propagates_connection_error(self, mock_load: MagicMock) -> None:
        mock_load.return_value = "Template {name}"
        self.mock_client.generate.side_effect = OllamaConnectionError("Offline")
        
        with self.assertRaises(OllamaConnectionError):
            self.ai_service.generate_professional_summary(
                name="Alice", target_role="Role", years_experience="1",
                skills=[], achievements=[]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)

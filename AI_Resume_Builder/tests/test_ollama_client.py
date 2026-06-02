"""
test_ollama_client.py — Unit tests for the Ollama integration.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ollama_client import OllamaClient, OllamaConnectionError, OllamaModelNotFoundError


class TestOllamaClient(unittest.TestCase):
    """Tests for Ollama API client."""

    def setUp(self) -> None:
        self.client = OllamaClient(base_url="http://test-server:11434", model="test-model")

    @patch("src.ollama_client.requests.Session.get")
    def test_check_health_success(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.assertTrue(self.client.check_health())
        mock_get.assert_called_once_with("http://test-server:11434/api/tags", timeout=5)

    @patch("src.ollama_client.requests.Session.get")
    def test_check_health_failure(self, mock_get: MagicMock) -> None:
        mock_get.side_effect = Exception("Connection error")
        self.assertFalse(self.client.check_health())

    @patch("src.ollama_client.requests.Session.get")
    def test_list_models_success(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "llama3"}, {"name": "mistral"}]
        }
        mock_get.return_value = mock_response

        models = self.client.list_models()
        self.assertEqual(models, ["llama3", "mistral"])

    @patch("src.ollama_client.requests.Session.post")
    def test_generate_success(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Generated text   "}
        mock_post.return_value = mock_response

        result = self.client.generate("Test prompt")
        self.assertEqual(result, "Generated text")
        
        # Verify payload
        call_args = mock_post.call_args[1]["json"]
        self.assertEqual(call_args["model"], "test-model")
        self.assertEqual(call_args["prompt"], "Test prompt")
        self.assertFalse(call_args["stream"])

    @patch("src.ollama_client.requests.Session.post")
    def test_generate_model_not_found(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        with self.assertRaises(OllamaModelNotFoundError):
            self.client.generate("Test prompt")

    @patch("src.ollama_client.requests.Session.post")
    def test_generate_connection_error(self, mock_post: MagicMock) -> None:
        import requests
        mock_post.side_effect = requests.RequestException("Network down")

        with self.assertRaises(OllamaConnectionError):
            self.client.generate("Test prompt")

    @patch("src.ollama_client.requests.Session.post")
    def test_chat_success(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"role": "assistant", "content": "Chat response  "}
        }
        mock_post.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        result = self.client.chat(messages)
        self.assertEqual(result, "Chat response")
        
        call_args = mock_post.call_args[1]["json"]
        self.assertEqual(call_args["messages"], messages)


if __name__ == "__main__":
    unittest.main(verbosity=2)

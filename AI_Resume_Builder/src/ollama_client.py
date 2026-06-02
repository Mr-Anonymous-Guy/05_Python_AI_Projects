"""
ollama_client.py — Ollama API client for LLM inference.

Provides a clean interface to Ollama's REST API with error handling,
retry logic, and response streaming support.
"""

import json
import logging
from typing import Any, Optional

import requests

from src.config import (
    DEFAULT_MODEL,
    MAX_TOKENS,
    OLLAMA_BASE_URL,
    TEMPERATURE,
    TOP_P,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────────────────────


class OllamaError(Exception):
    """Base exception for Ollama client errors."""

    pass


class OllamaConnectionError(OllamaError):
    """Raised when connection to Ollama fails."""

    pass


class OllamaModelNotFoundError(OllamaError):
    """Raised when the requested model is not available."""

    pass


# ──────────────────────────────────────────────────────────────
# Client
# ──────────────────────────────────────────────────────────────


class OllamaClient:
    """
    Client for interacting with Ollama's local LLM server.

    Supports synchronous generation with customizable parameters.
    """

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: int = 120,
    ) -> None:
        """
        Initialize the Ollama client.

        Args:
            base_url: Ollama server URL.
            model:    Default model to use for generation.
            timeout:  Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, endpoint: str) -> str:
        """Construct full API URL."""
        return f"{self.base_url}/api/{endpoint}"

    def check_health(self) -> bool:
        """
        Check if the Ollama server is reachable.

        Returns:
            True if server is healthy, False otherwise.
        """
        try:
            response = self.session.get(
                self._build_url("tags"),
                timeout=5,
            )
            return response.status_code == 200
        except Exception as exc:
            logger.error(f"Health check failed: {exc}")
            return False

    def list_models(self) -> list[str]:
        """
        List all available models on the Ollama server.

        Returns:
            List of model names.

        Raises:
            OllamaConnectionError: If the server is unreachable.
        """
        try:
            response = self.session.get(
                self._build_url("tags"),
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except requests.RequestException as exc:
            raise OllamaConnectionError(f"Failed to list models: {exc}")

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        top_p: float = TOP_P,
        system: Optional[str] = None,
    ) -> str:
        """
        Generate text from a prompt using the specified model.

        Args:
            prompt:      User prompt / instruction.
            model:       Model name (uses default if None).
            temperature: Sampling temperature (0.0 - 1.0).
            max_tokens:  Maximum tokens to generate.
            top_p:       Nucleus sampling threshold.
            system:      Optional system prompt.

        Returns:
            Generated text content.

        Raises:
            OllamaConnectionError: If the request fails.
            OllamaModelNotFoundError: If the model doesn't exist.
        """
        model_name = model or self.model

        payload: dict[str, Any] = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": top_p,
            },
        }

        if system:
            payload["system"] = system

        try:
            logger.info(f"Generating with model: {model_name}")
            response = self.session.post(
                self._build_url("generate"),
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code == 404:
                raise OllamaModelNotFoundError(
                    f"Model '{model_name}' not found. "
                    f"Run: ollama pull {model_name}"
                )

            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except requests.Timeout:
            raise OllamaConnectionError(
                f"Request timed out after {self.timeout}s"
            )
        except requests.RequestException as exc:
            raise OllamaConnectionError(f"Generation failed: {exc}")

    def chat(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = TEMPERATURE,
    ) -> str:
        """
        Multi-turn chat completion using Ollama's chat endpoint.

        Args:
            messages:    List of {"role": "user/assistant", "content": "..."}
            model:       Model name.
            temperature: Sampling temperature.

        Returns:
            Assistant's response text.

        Raises:
            OllamaConnectionError: If the request fails.
        """
        model_name = model or self.model

        payload = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }

        try:
            response = self.session.post(
                self._build_url("chat"),
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()

        except requests.RequestException as exc:
            raise OllamaConnectionError(f"Chat failed: {exc}")

    def __del__(self) -> None:
        """Clean up session on deletion."""
        if hasattr(self, "session"):
            self.session.close()

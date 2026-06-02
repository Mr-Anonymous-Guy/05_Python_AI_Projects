"""
llm_manager.py - Manages Chat Models via langchain-ollama.
"""

from typing import List
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage
from src.config import OLLAMA_BASE_URL, DEFAULT_CHAT_MODEL

class LLMManager:
    """Wrapper for Ollama Chat Models in EduSense."""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or DEFAULT_CHAT_MODEL
        self.llm = ChatOllama(
            model=self.model_name,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3
        )
        
    def generate(self, messages: List[BaseMessage]) -> BaseMessage:
        return self.llm.invoke(messages)
